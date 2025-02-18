from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Movne Chatbot V2")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat(request: ChatRequest):
    # Simple response for testing
    return {
        "response": f"Echo: {request.message} (in {request.language})"
    }
