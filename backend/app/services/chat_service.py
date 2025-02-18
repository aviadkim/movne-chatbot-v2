class ChatService:
    def __init__(self):
        self.initialized = True

    async def process_message(self, message: str, language: str) -> str:
        if language == "he":
            return f"קיבלתי את ההודעה: {message}"
        return f"Received message: {message}"
