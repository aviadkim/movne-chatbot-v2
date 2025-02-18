from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ....services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

class ChatResponse(BaseModel):
    response: str

chat_service = ChatService()

@router.post("/", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    try:
        response = await chat_service.process_message(request.message, request.language)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
