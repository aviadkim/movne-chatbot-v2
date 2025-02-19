from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

@app.get("/")
def root():
    return {"status": "online", "message": "Movne Chatbot is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    return {
        "response": "שלום! קיבלתי את ההודעה שלך: " + request.message if request.language == "he" 
        else "Hello! I received your message: " + request.message
    }
