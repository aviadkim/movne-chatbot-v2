from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

@app.get("/")
def root():
    return {"message": "Movne Bot API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    if request.language == "he":
        return {"response": f"קיבלתי את ההודעה: {request.message}"}
    return {"response": f"Received message: {request.message}"}
