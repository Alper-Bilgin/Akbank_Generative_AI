import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from backend.veri_yonetimi import verileri_yukle_ve_hazirla  # Bu satır eksikti
from backend.rag_pipeline import build_or_load_pipeline

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Sistem başlatılıyor...")

CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

# Vektör DB varsa yeniden yükleme yapma
if os.path.exists(CHROMA_PATH):
    print("Mevcut vektör DB bulundu, yükleniyor...")
    documents = []
else:
    print("Vektör DB yok, veriler yükleniyor (500 dökümanla test)...")
    documents = verileri_yukle_ve_hazirla()

rag_chain = build_or_load_pipeline(documents)
print("Sistem başarıyla başlatıldı.")


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def handle_chat(request: ChatRequest):
    if rag_chain is None:
        raise HTTPException(status_code=500, detail="Sistem düzgün başlatılamadı.")

    try:
        print(f"Soru alındı: {request.question}")
        response = rag_chain.invoke(request.question)
        return {"answer": response}
    except Exception as e:
        print(f"HATA: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/")
def root():
    return {"message": "Haber RAG API çalışıyor"}


@app.get("/documents/stats")
def get_document_stats():
    """Yüklenen döküman istatistiklerini döndürür"""
    if not os.path.exists(CHROMA_PATH):
        return {"error": "Vektör DB henüz oluşturulmamış"}

    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    embedding_function = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Tüm dökümanları çek
    docs = vectorstore.get()
    kategoriler = {}

    for metadata in docs['metadatas']:
        kategori = metadata.get('kategori', 'bilinmeyen')
        kategoriler[kategori] = kategoriler.get(kategori, 0) + 1

    return {
        "toplam_chunk": len(docs['ids']),
        "kategoriler": kategoriler
    }
