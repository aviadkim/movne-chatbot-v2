from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Optional, Dict
from app.core.config import settings
from app.db.session import get_db
from app.services.chat_service import AdvancedChatService
from pydantic import BaseModel
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    client_id: Optional[str] = None
    language: str = "he"
    context: Optional[Dict] = None


class ChatResponse(BaseModel):
    response: str
    client_id: str
    timestamp: str


# יצירת מופע יחיד של שירות הצ'אט
chat_service = AdvancedChatService()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """נקודת קצה ראשית לצ'אט"""
    try:
        # אם אין מזהה לקוח, צור אחד זמני
        if not request.client_id:
            request.client_id = f"guest_{datetime.utcnow().timestamp()}"

        # עיבוד ההודעה
        response = await chat_service.process_message(
            client_id=request.client_id,
            message=request.message,
            language=request.language,
            context=request.context,
        )

        # הוספת משימת רקע לניתוח השיחה
        background_tasks.add_task(
            analyze_conversation,
            client_id=request.client_id,
            message=request.message,
            response=response["response"],
        )

        return response

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        error_message = (
            "אירעה שגיאה, אנא נסה שוב"
            if request.language == "he"
            else "An error occurred, please try again"
        )
        raise HTTPException(status_code=500, detail=error_message)


@router.get("/history/{client_id}")
async def get_chat_history(
    client_id: str, limit: int = 10, db: Session = Depends(get_db)
):
    """שליפת היסטוריית שיחות"""
    try:
        history = chat_service.memory.get_client_history(
            client_id=client_id, limit=limit
        )
        return history
    except Exception as e:
        logger.error(f"Error fetching chat history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch chat history")


@router.get("/profile/{client_id}")
async def get_client_profile(client_id: str, db: Session = Depends(get_db)):
    """שליפת פרופיל לקוח"""
    try:
        profile = chat_service.memory.get_client_profile(client_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        return profile
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching client profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch client profile")


async def analyze_conversation(client_id: str, message: str, response: str):
    """ניתוח שיחה ברקע"""
    try:
        # כאן יכול להיות קוד לניתוח השיחה
        # למשל: זיהוי נושאים, ניתוח רגשות, זיהוי כוונות וכו'
        logger.info(f"Analyzing conversation for client {client_id}")
    except Exception as e:
        logger.error(f"Error analyzing conversation: {str(e)}")
