import os
import shutil
from hashlib import md5
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# .env dosyasından çevresel değişkenleri yükle (GOOGLE_API_KEY)
load_dotenv()

# ChromaDB'nin vektörleri saklayacağı klasör yolu
# __file__: Bu dosyanın (rag_pipeline.py) tam yolu
# Sonuç: backend/chroma_db/
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")


def _format_docs(docs):
    """
    Retriever'dan gelen Document objelerini string'e dönüştürür

    Args:
        docs (list[Document]): ChromaDB'den dönen benzer dökümanlar

    Returns:
        str: Her dökümanın page_content'i birleştirilmiş hali

    Örnek:
        Input: [Document(page_content="Haber 1"), Document(page_content="Haber 2")]
        Output: "Haber 1\n\nHaber 2"
    """
    # Her dökümanın text içeriğini al ve aralarına çift satır atla
    # LLM'e context olarak gönderilecek
    return "\n\n".join(d.page_content for d in docs)


def build_or_load_pipeline(documents, recreate_index=False, k=5):
    """
    RAG (Retrieval-Augmented Generation) pipeline'ını oluşturur veya mevcut olanı yükler

    Pipeline Adımları:
    1. Dökümanları chunk'lara böl (text splitting)
    2. Chunk'ları vektörleştir (embedding)
    3. ChromaDB'ye kaydet (vector database)
    4. Kullanıcı sorusuyla benzer chunk'ları bul (retrieval)
    5. Bulunan chunk'larla birlikte LLM'e prompt gönder (augmented generation)

    Args:
        documents (list[Document]): Veri setinden yüklenen dökümanlar (ilk çalıştırmada)
        recreate_index (bool): True ise mevcut vektör DB'yi sil ve yeniden oluştur
        k (int): Retrieval'da kaç benzer chunk getirilecek (varsayılan: 5)

    Returns:
        RunnableSequence: LangChain LCEL (LangChain Expression Language) chain'i

    Raises:
        RuntimeError: GOOGLE_API_KEY tanımlı değilse
    """
    # Google Gemini API anahtarı kontrolü
    # .env dosyasında GOOGLE_API_KEY=... olarak tanımlı olmalı
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("GOOGLE_API_KEY .env içinde tanımlı değil.")

    # --- 1. TEXT SPLITTING ---
    # Uzun dökümanları küçük chunk'lara böl
    # chunk_size=1000: Her chunk maksimum 1000 karakter
    # chunk_overlap=200: Chunk'lar arası 200 karakter örtüşme (context kaybını önler)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Token limiti için (embedding modeli max 512 token alabilir)
        chunk_overlap=200  # Cümle ortasında kesilmeyi önlemek için
    )

    # İlk çalıştırmada documents dolu, sonraki çalıştırmalarda boş liste
    docs = documents or []

    # Dökümanları chunk'lara böl
    # Her chunk bir Document objesi olur (page_content + metadata)
    chunks = text_splitter.split_documents(docs)

    # --- 2. EMBEDDING MODEL ---
    # Metinleri vektörlere (sayısal temsil) dönüştürecek model
    # paraphrase-multilingual: Türkçe destekli, anlamsal benzerlik için optimize
    # MiniLM-L12: 384 boyutlu vektörler üretir (hızlı ve etkili)
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # --- 3. VECTOR DATABASE YÖNETİMİ ---
    # recreate_index=True ise eski DB'yi sil (veri güncelleme durumunda)
    if recreate_index and os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)  # Klasörü komple sil

    # ChromaDB oluşturma veya yükleme
    if not os.path.exists(CHROMA_PATH):
        # İlk çalıştırma: Vektör DB'yi sıfırdan oluştur
        print("Vektör veritabanı oluşturuluyor... (Bu işlem biraz zaman alabilir)")

        # from_documents: Chunk'ları vektörleştir ve DB'ye kaydet
        # 1. Her chunk'ın page_content'i embedding_function'a gönderilir
        # 2. Dönen 384 boyutlu vektör ChromaDB'ye yazılır
        # 3. metadata (kategori) ile birlikte saklanır
        vectorstore = Chroma.from_documents(
            chunks,
            embedding_function,
            persist_directory=CHROMA_PATH  # Disk'e kalıcı olarak kaydet
        )
        print("Veritabanı başarıyla oluşturuldu.")
    else:
        # Sonraki çalıştırmalar: Mevcut DB'yi yükle
        print(f"Mevcut vektör veritabanı kullanılıyor: {CHROMA_PATH}")
        vectorstore = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embedding_function
        )

        # Eğer yeni chunk'lar varsa (incremental update)
        if chunks:
            try:
                # Yeni chunk'ları mevcut DB'ye ekle
                vectorstore.add_documents(chunks)
                print("Yeni parçalar eklendi.")
            except Exception as e:
                print(f"Parça ekleme hatası: {e}")

    # --- 4. RETRIEVER OLUŞTURMA ---
    # as_retriever(): VectorStore'u LangChain retriever'a dönüştür
    # search_kwargs={"k": 5}: Sorguya en benzer 5 chunk'ı getir
    # Benzerlik ölçütü: Cosine similarity (vektörler arası açı)
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    # --- 5. LLM (Large Language Model) ---
    # Google Gemini 2.5 Flash: Hızlı ve güncel model
    # temperature=0.2: Düşük randomness (tutarlı cevaplar için)
    #   - 0.0: Tamamen deterministik
    #   - 1.0: Maksimum yaratıcılık
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2
    )

    # --- 6. PROMPT TEMPLATE ---
    # LLM'e gönderilecek prompt şablonu
    # {context}: Retriever'dan gelen benzer chunk'lar
    # {question}: Kullanıcının sorusu
    template = (
        "Sana verilen metin parçalarını kullanarak soruları yanıtlayan bir haber asistanısın. "
        "Sadece aşağıdaki bağlamı kullanarak cevap ver. Cevabı bilmiyorsan, 'Bu konuda bilgim yok.' de.\n"
        "Bağlam:\n{context}\n\nSoru: {question}\nCevap:"
    )
    prompt = PromptTemplate.from_template(template)

    # --- 7. RAG CHAIN OLUŞTURMA (LCEL) ---
    # LangChain Expression Language ile pipeline tanımla
    # | operatörü: Verileri bir sonraki adıma geçirir (Unix pipe gibi)
    rag_chain = (
            {
                # "context" key'i için:
                # 1. retriever: Soruyla benzer chunk'ları bul
                # 2. RunnableLambda(_format_docs): Chunk'ları string'e dönüştür
                "context": retriever | RunnableLambda(_format_docs),

                # "question" key'i için:
                # RunnablePassthrough: Soruyu olduğu gibi geçir
                "question": RunnablePassthrough(),
            }
            | prompt  # Template'i doldur (context + question)
            | llm  # Gemini'ye gönder
            | StrOutputParser()  # LLM çıktısını string'e parse et
    )

    # Chain'i döndür (invoke() metodu ile çağrılabilir)
    return rag_chain
