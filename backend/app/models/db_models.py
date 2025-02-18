from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, index=True)
    preferred_language = Column(String(2), default="he")
    created_at = Column(DateTime, default=datetime.utcnow)
    last_active = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON)
    conversations = relationship("Conversation", back_populates="client")

    __table_args__ = (Index("idx_client_last_active", last_active),)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, ForeignKey("clients.client_id"))
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    language = Column(String(2))
    messages = relationship("Message", back_populates="conversation")
    client = relationship("Client", back_populates="conversations")

    __table_args__ = (Index("idx_conversation_client", client_id, started_at),)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(
        Integer, ForeignKey("conversations.id", ondelete="CASCADE")
    )
    role = Column(String)  # 'user' או 'assistant'
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)  # שדה לנתוני ניתוח נוספים
    conversation = relationship("Conversation", back_populates="messages")

    __table_args__ = (Index("idx_message_conversation", conversation_id, created_at),)


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True)
    title_he = Column(String)
    title_en = Column(String)
    content_he = Column(Text)
    content_en = Column(Text)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON, nullable=True)

    def to_dict(self, language="he"):
        return {
            "id": self.id,
            "title": self.title_he if language == "he" else self.title_en,
            "content": self.content_he if language == "he" else self.content_en,
            "category": self.category,
            "updated_at": self.updated_at.isoformat(),
        }
