from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .models.chat_model import MovneChat
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Movne Chatbot API")

# Configure CORS
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

@app.get("/health")
async def health_check():
    try:
        if not chat_model.is_initialized():
            raise HTTPException(status_code=500, detail="Chat model not initialized")
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    try:
        response = chat_model.generate_response(request.message, request.language)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
