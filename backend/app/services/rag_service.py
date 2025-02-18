from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
import logging

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
    def add_documents(self, texts: List[str], metadatas: List[dict] = None):
        try:
            embeddings = self.model.encode(texts).tolist()
            ids = [str(i) for i in range(len(texts))]
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas or [{}] * len(texts),
                ids=ids
            )
            logger.info(f"Added {len(texts)} documents to RAG system")
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    def get_relevant_context(self, query: str, n_results: int = 3) -> List[str]:
        try:
            query_embedding = self.model.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            return results["documents"][0]
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            return []
