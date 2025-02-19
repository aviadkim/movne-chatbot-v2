from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List

class RAGSettings(BaseSettings):
    # Vector store settings
    VECTOR_STORE_PATH: Path = Path("data/vector_store")
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"  # Multilingual model
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    
    # Document processing
    SUPPORTED_LANGUAGES: List[str] = ["en", "he"]
    SUPPORTED_DOC_TYPES: List[str] = [
        "product_guide",
        "regulation",
        "marketing_material",
        "risk_disclosure",
        "term_sheet"
    ]
    
    # Retrieval settings
    MAX_RELEVANT_CHUNKS: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    
    # Context management
    MAX_CONTEXT_WINDOW: int = 4096  # Maximum tokens for context window
    CONVERSATION_MEMORY_K: int = 5  # Number of recent messages to keep in memory
    
    # Regulatory compliance
    COMPLIANCE_CHECK_ENABLED: bool = True
    RISK_DISCLOSURE_REQUIRED: bool = True
    
    class Config:
        env_prefix = "RAG_"

rag_settings = RAGSettings()