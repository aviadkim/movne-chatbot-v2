import httpx
from .vectorstore import VectorStore
from ..core.config import settings

class ChatService:
    def __init__(self):
        self.vector_store = VectorStore()
        self.ollama_url = f"{settings.OLLAMA_HOST}/api/generate"
        
    async def _generate_response(self, prompt: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.ollama_url,
                json={
                    "model": settings.OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False
                }
            )
            return response.json()["response"]

    async def get_chat_response(self, message: str) -> str:
        # Retrieve relevant context
        context = self.vector_store.search(message)
        
        # Create bilingual prompt
        prompt = f"""Use the following context to answer the question. Answer in the same language as the question.
If the context doesn't help, just say you don't know.

Context:
{' '.join(context)}

Question: {message}

Answer:"""

        return await self._generate_response(prompt)
