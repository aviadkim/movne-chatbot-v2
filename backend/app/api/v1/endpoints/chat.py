from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ...services.chat import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    try:
        response = await chat_service.get_chat_response(message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
