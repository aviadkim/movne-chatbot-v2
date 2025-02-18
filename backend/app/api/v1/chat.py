from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.chat_service import AdvancedChatService

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        chat_service = AdvancedChatService()
        response = await chat_service.process_message(request.message, request.language)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
