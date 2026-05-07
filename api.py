from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import engine

app = FastAPI(title="MDP Group AI API")

# Web sitesinin (Vercel) bu API'ye erişebilmesi için güvenlik izinleri
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tüm sitelerden gelen isteklere izin ver
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gelen sorunun formatı
class ChatRequest(BaseModel):
    message: str

# API Uç Noktası
@app.post("/ask")
async def ask_bot(request: ChatRequest):
    # Kullanıcının sorusunu rag_engine'e gönder ve cevabı al
    answer = engine.ask_to_bot(request.message)
    return {"reply": answer}