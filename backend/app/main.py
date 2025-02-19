from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .models.chat_model import chat_model
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporarily comment out static files for local development
# app.mount("/static", StaticFiles(directory="/app/static"), name="static")

class ChatRequest(BaseModel):
    message: str
    language: str = "he"
    is_qualified: bool = False

@app.get("/")
def root():
    return {"status": "online", "message": "Movne Chatbot is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    try:
        response = chat_model.generate_response(request.message, request.language, request.is_qualified)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    if full_path.startswith("api/"):
        return {"error": "API endpoint not found"}
    # Temporarily return API error for all non-API routes during local development
    return {"error": "Frontend not available in local development"}
