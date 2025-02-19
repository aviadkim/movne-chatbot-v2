from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from .config import settings

app = FastAPI(
    title="Movne Chatbot",
    description="AI-powered chatbot for Movne - משרד החינוך",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS with environment variables
origins = settings.ALLOWED_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

@app.get("/")
async def root():
    return {
        "name": "Movne Chatbot",
        "version": "1.0.0",
        "status": "active",
        "documentation": "/docs",
        "health_check": "/health",
        "chat_endpoint": "/api/chat"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    if request.language == "he":
        return {"response": f"קיבלתי את ההודעה: {request.message}"}
    return {"response": f"Received message: {request.message}"}
