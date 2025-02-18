from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.chat_service import ChatService
from app.services.rag_service import RAGService

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Check database connection
        db.execute("SELECT 1")
        
        # Check services initialization
        chat_service = ChatService()
        rag_service = RAGService()
        
        return {
            "status": "healthy",
            "database": "connected",
            "chat_service": "initialized",
            "rag_service": "initialized"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }
