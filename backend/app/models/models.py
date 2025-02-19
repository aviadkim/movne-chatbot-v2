from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    risk_profile = Column(String)  # Conservative, Moderate, Aggressive
    investment_goals = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    conversations = relationship("Conversation", back_populates="client")
    investments = relationship("ClientInvestment", back_populates="client")

class StructuredProduct(Base):
    __tablename__ = "structured_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    risk_level = Column(String)  # Low, Medium, High
    min_investment = Column(Float)
    term_length = Column(Integer)  # in months
    expected_return = Column(Float)
    currency = Column(String)
    is_active = Column(Boolean, default=True)
    product_rules = Column(JSON)  # Store complex rules as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    investments = relationship("ClientInvestment", back_populates="product")

class ClientInvestment(Base):
    __tablename__ = "client_investments"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    product_id = Column(Integer, ForeignKey("structured_products.id"))
    amount = Column(Float)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())
    maturity_date = Column(DateTime(timezone=True))
    status = Column(String)  # Active, Matured, Cancelled
    
    client = relationship("Client", back_populates="investments")
    product = relationship("StructuredProduct", back_populates="investments")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True))
    context = Column(JSON)  # Store conversation context and metadata
    
    client = relationship("Client", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    content = Column(Text)
    role = Column(String)  # user or assistant
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON)  # Store additional message metadata
    
    conversation = relationship("Conversation", back_populates="messages")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    document_type = Column(String)  # product_guide, regulation, marketing_material
    language = Column(String)
    metadata = Column(JSON)  # Store document metadata and embeddings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())