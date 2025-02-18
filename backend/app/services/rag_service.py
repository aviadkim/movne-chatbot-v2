from typing import List, Optional
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
import pickle
from pathlib import Path
from app.core.config import settings

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
        self.index = None
        self.documents = []
        self.initialize_index()
        
    def initialize_index(self):
        try:
            index_path = settings.KNOWLEDGE_BASE_PATH / "faiss_index.pkl"
            docs_path = settings.KNOWLEDGE_BASE_PATH / "documents.pkl"
            
            if index_path.exists() and docs_path.exists():
                with open(index_path, 'rb') as f:
                    self.index = pickle.load(f)
                with open(docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                logger.info("Loaded existing index and documents")
            else:
                dimension = self.model.get_sentence_embedding_dimension()
                self.index = faiss.IndexFlatL2(dimension)
                logger.info("Created new FAISS index")
                
        except Exception as e:
            logger.error(f"Error initializing FAISS index: {str(e)}")
            raise

    async def get_relevant_docs(self, query: str, language: str, n_results: int = 3) -> List[str]:
        try:
            if not self.index or self.index.ntotal == 0:
                return []
                
            # Get query embedding
            query_embedding = self.model.encode(query)
            query_embedding = np.array([query_embedding]).astype('float32')
            
            # Search
            D, I = self.index.search(query_embedding, n_results)
            
            # Get relevant documents
            relevant_docs = [self.documents[i] for i in I[0] if i < len(self.documents)]
            
            return relevant_docs
            
        except Exception as e:
            logger.error(f"Error retrieving relevant docs: {str(e)}")
            return []

    async def add_document(self, text: str, metadata: dict):
        try:
            # Get embedding
            embedding = self.model.encode(text)
            embedding = np.array([embedding]).astype('float32')
            
            # Add to index
            self.index.add(embedding)
            self.documents.append(text)
            
            # Save index and documents
            index_path = settings.KNOWLEDGE_BASE_PATH / "faiss_index.pkl"
            docs_path = settings.KNOWLEDGE_BASE_PATH / "documents.pkl"
            
            with open(index_path, 'wb') as f:
                pickle.dump(self.index, f)
            with open(docs_path, 'wb') as f:
                pickle.dump(self.documents, f)
                
            logger.info("Document added and index saved successfully")
            
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            raise
