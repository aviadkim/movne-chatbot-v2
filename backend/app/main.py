from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .models.chat_model import chat_model
from .db.session import test_connection
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
    health_status = {
        "status": "initializing",
        "database": "unknown",
        "model": "unknown",
        "details": {}
    }
    
    # Check database connection
    try:
        if test_connection():
            health_status["database"] = "connected"
        else:
            health_status["database"] = "failed"
            health_status["details"]["database_error"] = "Could not connect to database"
    except Exception as e:
        health_status["database"] = "error"
        health_status["details"]["database_error"] = str(e)
    
    # Check chat model initialization
    try:
        if chat_model.is_initialized():
            health_status["model"] = "initialized"
        else:
            health_status["model"] = "failed"
            health_status["details"]["model_error"] = "Model not initialized"
    except Exception as e:
        health_status["model"] = "error"
        health_status["details"]["model_error"] = str(e)
    
    # Determine overall status
    if health_status["database"] == "connected" and health_status["model"] == "initialized":
        health_status["status"] = "healthy"
    else:
        health_status["status"] = "unhealthy"
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status

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
