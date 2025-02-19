from typing import List, Dict, Any
from pathlib import Path
from sqlalchemy.orm import Session
from ..models.models import Document
from ..core.rag_config import rag_settings
from .rag_service import RAGService
import os
import json

class DocumentProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.rag_service = RAGService(db)
    
    def process_document_file(self, file_path: Path, document_type: str, language: str, metadata: Dict[str, Any] = None) -> Document:
        """Process a document file and store it in the database and vector store"""
        if document_type not in rag_settings.SUPPORTED_DOC_TYPES:
            raise ValueError(f"Unsupported document type: {document_type}")
        
        if language not in rag_settings.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {language}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create document record
        document = Document(
            title=file_path.stem,
            content=content,
            document_type=document_type,
            language=language,
            metadata=metadata or {}
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        # Process document for vector store
        self.rag_service.process_document(document)
        
        return document
    
    def batch_process_directory(self, directory_path: Path, document_type: str = None) -> List[Document]:
        """Process all documents in a directory"""
        processed_documents = []
        
        for file_path in directory_path.glob('**/*'):
            if file_path.is_file() and file_path.suffix in ['.txt', '.md', '.json']:
                metadata = {}
                
                # If it's a JSON file, try to extract metadata
                if file_path.suffix == '.json':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        content_file = data.get('content_file')
                        if content_file:
                            file_path = directory_path / content_file
                            metadata = data.get('metadata', {})
                
                # Determine document type and language
                doc_type = document_type or self._infer_document_type(file_path, metadata)
                language = metadata.get('language', self._detect_language(file_path))
                
                try:
                    document = self.process_document_file(
                        file_path=file_path,
                        document_type=doc_type,
                        language=language,
                        metadata=metadata
                    )
                    processed_documents.append(document)
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
        
        return processed_documents
    
    def _infer_document_type(self, file_path: Path, metadata: Dict[str, Any]) -> str:
        """Infer document type from file path or metadata"""
        # First check metadata
        if 'document_type' in metadata:
            return metadata['document_type']
        
        # Then check file path
        path_str = str(file_path).lower()
        if 'regulation' in path_str or 'compliance' in path_str:
            return 'regulation'
        elif 'product' in path_str and 'guide' in path_str:
            return 'product_guide'
        elif 'marketing' in path_str:
            return 'marketing_material'
        elif 'risk' in path_str:
            return 'risk_disclosure'
        elif 'term' in path_str and 'sheet' in path_str:
            return 'term_sheet'
        
        raise ValueError(f"Could not infer document type for {file_path}")
    
    def _detect_language(self, file_path: Path) -> str:
        """Detect document language"""
        # This is a simple implementation. In production, use a proper language detection library
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(1000)  # Read first 1000 characters
        
        # Check for Hebrew characters
        if any('\u0590' <= c <= '\u05FF' for c in content):
            return 'he'
        return 'en'  # Default to English