import requests
import logging
import sys
from pathlib import Path
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BotHealthChecker:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        self.status = {
            "database": False,
            "rag_system": False,
            "chat_service": False,
            "api": False,
            "frontend": False
        }

    def check_api_health(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/health")
            self.status["api"] = response.status_code == 200
            return self.status["api"]
        except requests.RequestException as e:
            logger.error(f"API health check failed: {str(e)}")
            return False

    def test_chat_endpoint(self) -> bool:
        try:
            test_message = {"message": "test message", "conversation_id": "test"}
            response = requests.post(f"{self.base_url}/api/v1/chat", json=test_message)
            self.status["chat_service"] = response.status_code == 200
            return self.status["chat_service"]
        except requests.RequestException as e:
            logger.error(f"Chat endpoint test failed: {str(e)}")
            return False

    def check_rag_system(self) -> bool:
        try:
            test_query = {"query": "test query"}
            response = requests.post(f"{self.base_url}/api/v1/rag/query", json=test_query)
            self.status["rag_system"] = response.status_code == 200
            return self.status["rag_system"]
        except requests.RequestException as e:
            logger.error(f"RAG system test failed: {str(e)}")
            return False

    def check_frontend(self) -> bool:
        try:
            response = requests.get(self.frontend_url)
            self.status["frontend"] = response.status_code == 200
            return self.status["frontend"]
        except requests.RequestException as e:
            logger.error(f"Frontend check failed: {str(e)}")
            return False

    def print_status(self):
        print("\n=== Bot Health Check Results ===")
        for component, status in self.status.items():
            icon = "✅" if status else "❌"
            print(f"{icon} {component.replace('_', ' ').title()}: {'Working' if status else 'Failed'}")

    def run_all_checks(self) -> bool:
        logger.info("Starting bot health checks...")
        
        checks = [
            self.check_api_health(),
            self.test_chat_endpoint(),
            self.check_rag_system(),
            self.check_frontend()
        ]
        
        self.print_status()
        return all(checks)

if __name__ == "__main__":
    checker = BotHealthChecker()
    success = checker.run_all_checks()
    
    if not success:
        logger.error("Bot health check failed!")
        sys.exit(1)
    else:
        logger.info("All bot components are working correctly!")
