from fastapi import FastAPI
happ = FastAPI()
@app.post('/api/v1/chat')
async def chat(message: str, language: str):
    return {'response': f'Received: {message} in {language}'}
