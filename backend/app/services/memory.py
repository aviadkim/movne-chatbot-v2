from typing import Dict, List

class ConversationMemory:
    def __init__(self):
        self.conversations: Dict[str, List[dict]] = {}

    def add_message(self, session_id: str, message: dict):
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        self.conversations[session_id].append(message)

    def get_history(self, session_id: str) -> List[dict]:
        return self.conversations.get(session_id, [])
