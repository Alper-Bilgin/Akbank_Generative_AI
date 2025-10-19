import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from backend.veri_yonetimi import verileri_yukle_ve_hazirla
from backend.rag_pipeline import build_or_load_pipeline

# FastAPI uygulaması oluştur
app = FastAPI()

# CORS (Cross-Origin Resource Sharing) middleware'i ekle
# Frontend'in farklı bir port'tan (örn: 3000) backend'e (örn: 8000) istek atabilmesi için gerekli
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tüm originlere izin ver (production'da spesifik domainler belirtilmeli)
    allow_credentials=True,  # Cookie ve authentication header'larına izin ver
    allow_methods=["*"],  # Tüm HTTP metodlarına (GET, POST, PUT, DELETE) izin ver
    allow_headers=["*"],  # Tüm header'lara izin ver
)

print("Sistem başlatılıyor...")

# ChromaDB'nin persist edileceği klasör yolu
# __file__ bu dosyanın (main.py) tam yolunu verir
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

# Vektör veritabanı kontrolü
# Eğer daha önce oluşturulmuş bir ChromaDB varsa yeniden veri işleme yapma
if os.path.exists(CHROMA_PATH):
    print("Mevcut vektör DB bulundu, yükleniyor...")
    documents = []  # Boş liste, çünkü vektörler zaten DB'de
else:
    print("Vektör DB yok, veriler yükleniyor...")
    # Kaggle'dan veriyi indir, temizle ve chunk'lara böl
    documents = verileri_yukle_ve_hazirla()

# RAG (Retrieval-Augmented Generation) pipeline'ını oluştur veya yükle
# documents: Yeni yüklenecek dökümanlar (varsa)
# ChromaDB'den vektörleri yükler ve LangChain chain'i kurar
rag_chain = build_or_load_pipeline(documents)
print("Sistem başarıyla başlatıldı.")


# Pydantic model: API'ye gelen istek formatını tanımlar
# request.question şeklinde erişilebilir
class ChatRequest(BaseModel):
    question: str  # Kullanıcının sorusu


@app.post("/chat")
def handle_chat(request: ChatRequest):
    """
    Ana chat endpoint'i
    Frontend'den gelen soruyu alır, RAG pipeline'a gönderir ve cevabı döndürür
    """
    # Pipeline başlatılamadıysa hata fırlat
    if rag_chain is None:
        raise HTTPException(status_code=500, detail="Sistem düzgün başlatılamadı.")

    try:
        print(f"Soru alındı: {request.question}")
        # RAG chain'i çalıştır:
        # 1. Soruyla alakalı dökümanları ChromaDB'den bul (retrieval)
        # 2. Bulunan dökümanlarla birlikte LLM'e prompt gönder (augmentation)
        # 3. LLM'den cevap al (generation)
        response = rag_chain.invoke(request.question)
        return {"answer": response}
    except Exception as e:
        print(f"HATA: {e}")
        # Hata durumunda 500 Internal Server Error döndür
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
def root():
    """
    Health check endpoint'i
    API'nin çalışıp çalışmadığını kontrol etmek için
    """
    return {"message": "Haber RAG API çalışıyor"}


@app.get("/documents/stats")
def get_document_stats():
    """
    ChromaDB'deki döküman istatistiklerini döndürür
    - Toplam chunk sayısı
    - Kategorilere göre dağılım
    """
    # Vektör DB henüz oluşturulmadıysa hata döndür
    if not os.path.exists(CHROMA_PATH):
        return {"error": "Vektör DB henüz oluşturulmamış"}

    # Embedding fonksiyonunu yeniden oluştur (ChromaDB okumak için gerekli)
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    # Aynı embedding modelini kullan (tutarlılık için önemli)
    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # ChromaDB'yi yükle
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,  # Vektörlerin saklandığı klasör
        embedding_function=embedding_function  # Embedding fonksiyonu
    )

    # Tüm dökümanları ve metadata'larını çek
    # docs['ids']: Chunk ID'leri
    # docs['metadatas']: Her chunk'ın metadata'sı (kategori, tarih, vb.)
    # docs['documents']: Chunk'ların text içerikleri
    docs = vectorstore.get()

    # Kategorilere göre chunk sayılarını hesapla
    kategoriler = {}
    for metadata in docs['metadatas']:
        kategori = metadata.get('kategori', 'bilinmeyen')  # kategori yoksa 'bilinmeyen'
        kategoriler[kategori] = kategoriler.get(kategori, 0) + 1

    # İstatistikleri JSON olarak döndür
    return {
        "toplam_chunk": len(docs['ids']),  # Toplam chunk sayısı
        "kategoriler": kategoriler  # Her kategorideki chunk sayısı
    }
