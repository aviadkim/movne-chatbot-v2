from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings
from datetime import datetime
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class MemoryStore:
    def __init__(self, persist_directory: Path):
        self.client = chromadb.Client(
            Settings(
                persist_directory=str(persist_directory),
                chroma_db_impl="duckdb+parquet",
            )
        )

        # יצירת קולקציות לסוגי מידע שונים
        self.conversation_collection = self.client.get_or_create_collection(
            name="conversations", metadata={"description": "User conversation history"}
        )

        self.profile_collection = self.client.get_or_create_collection(
            name="profiles", metadata={"description": "User profiles and preferences"}
        )

    def add_conversation(
        self,
        client_id: str,
        message: str,
        response: str,
        language: str,
        metadata: Optional[Dict] = None,
    ):
        """הוספת שיחה למאגר"""
        try:
            conversation_data = {
                "message": message,
                "response": response,
                "language": language,
                "timestamp": datetime.utcnow().isoformat(),
            }
            if metadata:
                conversation_data.update(metadata)

            self.conversation_collection.add(
                documents=[json.dumps(conversation_data)],
                metadatas=[{"client_id": client_id, "language": language}],
                ids=[f"conv_{client_id}_{datetime.utcnow().timestamp()}"],
            )
            logger.info(f"Added conversation for client {client_id}")
        except Exception as e:
            logger.error(f"Error adding conversation: {str(e)}")
            raise

    def get_client_history(
        self, client_id: str, limit: int = 10, language: Optional[str] = None
    ) -> List[Dict]:
        """שליפת היסטוריית שיחות של לקוח"""
        try:
            query = {"client_id": client_id}
            if language:
                query["language"] = language

            results = self.conversation_collection.query(
                query_texts=[""], where=query, limit=limit
            )

            conversations = []
            for doc in results["documents"][0]:
                conversations.append(json.loads(doc))

            return sorted(conversations, key=lambda x: x["timestamp"], reverse=True)
        except Exception as e:
            logger.error(f"Error fetching client history: {str(e)}")
            return []

    def update_client_profile(self, client_id: str, profile_data: Dict):
        """עדכון פרופיל לקוח"""
        try:
            self.profile_collection.upsert(
                documents=[json.dumps(profile_data)],
                metadatas=[{"client_id": client_id}],
                ids=[f"profile_{client_id}"],
            )
            logger.info(f"Updated profile for client {client_id}")
        except Exception as e:
            logger.error(f"Error updating client profile: {str(e)}")
            raise

    def get_client_profile(self, client_id: str) -> Optional[Dict]:
        """שליפת פרופיל לקוח"""
        try:
            results = self.profile_collection.query(
                query_texts=[""], where={"client_id": client_id}, limit=1
            )

            if results["documents"][0]:
                return json.loads(results["documents"][0][0])
            return None
        except Exception as e:
            logger.error(f"Error fetching client profile: {str(e)}")
            return None
