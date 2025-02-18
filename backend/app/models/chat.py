from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    message = Column(Text)
    response = Column(Text)
    language = Column(String(2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
