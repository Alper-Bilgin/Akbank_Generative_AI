from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .veri_yonetimi import verileri_yukle_ve_hazirla
from .rag_pipeline import build_or_load_pipeline
import sys


print("Sistem başlatılıyor...")
documents = verileri_yukle_ve_hazirla()
rag_chain = None
if documents:
    rag_chain = build_or_load_pipeline(documents)
    print("Sistem başarıyla başlatıldı.")
else:
    print("HATA: Veri yüklenemediği için sistem başlatılamadı.", file=sys.stderr)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def handle_chat(request: ChatRequest):
    if rag_chain is None:
        return {"error": "Sistem düzgün başlatılamadı. Lütfen sunucu loglarını kontrol edin."}, 500

    try:
        response = rag_chain.invoke(request.question)
        return {"answer": response}
    except Exception as e:
        return {"error": str(e)}, 500


@app.get("/")
def read_root():
    return {"status": "API çalışıyor"}