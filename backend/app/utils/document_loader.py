import os
from typing import List
from ..services.vectorstore import VectorStore

def load_documents(directory: str) -> List[str]:
    texts = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
                text = f.read()
                # Split into smaller chunks if needed
                chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
                texts.extend(chunks)
    return texts

def initialize_knowledge_base(docs_directory: str):
    vector_store = VectorStore()
    texts = load_documents(docs_directory)
    vector_store.add_documents(texts)
