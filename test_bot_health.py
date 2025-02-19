import requests
import logging
import sys
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BotHealthChecker:
    def __init__(self):
        # Get base URL from environment or use default
        self.base_url = os.getenv('API_URL', 'http://localhost:8000')
        if os.getenv('RAILWAY_STATIC_URL'):
            self.base_url = os.getenv('RAILWAY_STATIC_URL')
        
        self.status = {
            "api": False,
            "chat_service": False
        }

    def check_api_health(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/health")
            self.status["api"] = response.status_code == 200
            logger.info(f"API Health check: {response.json()}")
            return self.status["api"]
        except requests.RequestException as e:
            logger.error(f"API health check failed: {str(e)}")
            return False

    def test_chat_endpoint(self) -> bool:
        try:
            test_message = {"message": "test message", "language": "he"}
            response = requests.post(f"{self.base_url}/api/chat", json=test_message)
            self.status["chat_service"] = response.status_code == 200
            if response.status_code == 200:
                logger.info(f"Chat response: {response.json()}")
            return self.status["chat_service"]
        except requests.RequestException as e:
            logger.error(f"Chat endpoint test failed: {str(e)}")
            return False

    def print_status(self):
        print("\n=== Bot Health Check Results ===")
        for component, status in self.status.items():
            icon = "✅" if status else "❌"
            print(f"{icon} {component.replace('_', ' ').title()}: {'Working' if status else 'Failed'}")

    def run_all_checks(self) -> bool:
        logger.info(f"Starting bot health checks on {self.base_url}...")
        
        checks = [
            self.check_api_health(),
            self.test_chat_endpoint()
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
        sys.exit(0)
