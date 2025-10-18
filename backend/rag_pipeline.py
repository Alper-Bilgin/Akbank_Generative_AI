import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
CHROMA_PATH = "chroma_db"


def build_or_load_pipeline(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    # --- DEĞİŞİKLİK 2: Google yerine HuggingFace Embedding Modeli kullan ---
    # Model ilk defa çalıştırıldığında internetten indirilir ve .cache klasörüne kaydedilir.
    # Sonraki çalıştırmalarda çevrimdışı olarak kullanılır.
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_function = HuggingFaceEmbeddings(model_name=model_name)
    # -------------------------------------------------------------------------

    if not os.path.exists(CHROMA_PATH):
        print("Vektör veritabanı oluşturuluyor... (Bu işlem biraz zaman alabilir)")
        vectorstore = Chroma.from_documents(chunks, embedding_function, persist_directory=CHROMA_PATH)
        print("Veritabanı başarıyla oluşturuldu.")
    else:
        print("Mevcut vektör veritabanı kullanılıyor.")

    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    retriever = vectorstore.as_retriever(search_kwargs={'k': 3})

    # Not: LLM olarak hala Gemini'yi kullanıyoruz, sadece embedding işlemini yerel yaptık.
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)

    template = """Sana verilen metin parçalarını kullanarak soruları yanıtlayan bir haber asistanısın. Sadece aşağıdaki bağlamı kullanarak cevap ver. Cevabı bilmiyorsan, 'Bu konuda bilgim yok.' de.
    Bağlam: {context}
    Soru: {question}
    Cevap:"""
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain