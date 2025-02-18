class RAGService:
    def __init__(self):
        self.initialized = True

    async def query(self, text: str) -> str:
        return f"RAG response for: {text}"
