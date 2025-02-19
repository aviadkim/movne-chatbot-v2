from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="/app/static"), name="static")

class ChatRequest(BaseModel):
    message: str
    language: str = "he"

@app.get("/")
def root():
    return {"status": "online", "message": "Movne Chatbot is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    return {
        "response": "שלום! קיבלתי את ההודעה שלך: " + request.message if request.language == "he" 
        else "Hello! I received your message: " + request.message
    }

@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    if full_path.startswith("api/"):
        return {"error": "API endpoint not found"}
    return FileResponse("/app/static/index.html")
