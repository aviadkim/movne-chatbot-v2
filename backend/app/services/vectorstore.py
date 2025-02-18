import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from ..core.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(
            path=str(settings.KNOWLEDGE_BASE_PATH),
            settings=ChromaSettings(allow_reset=True)
        )
        self.collection = self.client.get_or_create_collection("documents")
        self.encoder = SentenceTransformer(str(settings.MODEL_PATH))
    
    def add_documents(self, texts: list[str], metadatas: list[dict] = None):
        embeddings = self.encoder.encode(texts).tolist()
        ids = [str(i) for i in range(len(texts))]
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas or [{}] * len(texts),
            ids=ids
        )
    
    def search(self, query: str, n_results: int = 3):
        query_embedding = self.encoder.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        return results["documents"][0]
