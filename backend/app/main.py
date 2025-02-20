from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from .models.chat_model import MovneChat
import os

app = FastAPI(title="Movne Chatbot API")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chat model
chat_model = MovneChat()

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    try:
        response = chat_model.generate_response(request.message, request.language)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy" if chat_model.is_initialized() else "unhealthy"}

# Serve frontend static files (mount last)
app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="static")