import os
import subprocess
import time
import json
import re
from typing import Dict, Optional, List
import logging
from datetime import datetime
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='movne_chatbot_agent_log.log'
)

class MovneChatbotAgent:
    def __init__(self, github_repo: str, railway_project_id: str, openai_api_key: Optional[str] = None):
        """
        Initialize the Movne Chatbot Agent with project details and credentials.
        
        Args:
            github_repo: GitHub repository URL (e.g., "https://github.com/aviadkim/movne-chatbot-v2.git")
            railway_project_id: Railway project ID (e.g., from your Railway dashboard)
            openai_api_key: OpenAI API key (optional; can be loaded from env var for security)
        """
        self.github_repo = github_repo
        self.railway_project_id = railway_project_id
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required. Set it as an argument or in the OPENAI_API_KEY environment variable.")
        
        self.project_dir = Path.cwd()
        self._check_prerequisites()

    def _check_prerequisites(self) -> None:
        """Check if Git, Railway CLI, Python, and git-filter-repo are installed."""
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True, text=True)
            subprocess.run(['python', '--version'], check=True, capture_output=True, text=True)
            subprocess.run([sys.executable, '-m', 'pip', 'show', 'git-filter-repo'], check=True, capture_output=True, text=True)
            logging.info("Git, Python, and git-filter-repo are installed.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Missing prerequisites: {e}")
            if "git-filter-repo" in str(e):
                logging.info("Installing git-filter-repo...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', 'git-filter-repo'], check=True)
            else:
                raise Exception("Please install Git and Python before proceeding.")

        try:
            # Use railway.exe from scoop installation
            railway_path = r"C:\Users\Aviad\scoop\apps\railway\current\railway.exe"
            subprocess.run([railway_path, '--version'], check=True, capture_output=True, text=True)
            logging.info("Railway CLI is installed.")
        except subprocess.CalledProcessError as e:
            logging.error("Railway CLI is not installed or not accessible.")
            print("Error: Railway CLI is not installed or not accessible at C:\\Users\\Aviad\\scoop\\apps\\railway\\current\\railway.exe.\n" +
                  "Please ensure the Railway CLI is installed via Scoop and the path is correct.\n" +
                  "If using a different installation (e.g., npm), update the script to use the correct path or executable.\n\n" +
                  "After installation, restart your terminal and run the script again.")
            raise Exception("Railway CLI is required for deployment.")

    def _ensure_project_structure(self) -> Dict[str, bool]:
        """Check and ensure the project structure and files exist."""
        required_files = {
            "requirements.txt": False,
            "app.py": False,
            "Dockerfile": False,
            ".gitignore": False
        }
        for file, exists in required_files.items():
            required_files[file] = (self.project_dir / file).exists()
        
        missing = [f for f, exists in required_files.items() if not exists]
        if missing:
            logging.warning(f"Missing files in project: {', '.join(missing)}")
            self._create_missing_files(missing)
        
        return required_files

    def _create_missing_files(self, missing_files: List[str]) -> None:
        """Create missing project files with default content using UTF-8 encoding."""
        for file in missing_files:
            if file == "requirements.txt":
                content = "openai\nflask\npython-dotenv\n"
                (self.project_dir / file).write_text(content, encoding='utf-8')
                logging.info(f"Created {file} with default dependencies.")
            elif file == "app.py":
                content = """
import os
import openai

openai.api_key = os.environ.get("OPENAI_API_KEY")

def respond_to_query(query: str, language: str = "en") -> str:
    if language == "he":
        prompt = f"תגובה בעברית: {query}"
    else:
        prompt = f"Response in English: {query}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message['content'].strip()

if __name__ == "__main__":
    while True:
        query = input("Ask a question (or 'quit' to exit, 'he' for Hebrew): ")
        if query.lower() == 'quit':
            break
        language = "he" if query.lower() == 'he' else "en"
        if language == "he":
            query = input("שאלה (או 'יציאה' לצאת): ")
            if query.lower() == 'יציאה':
                break
        print(respond_to_query(query, language))
                """
                (self.project_dir / file).write_text(content, encoding='utf-8')
                logging.info(f"Created {file} with a basic chatbot implementation.")
            elif file == "Dockerfile":
                content = """
FROM python:3.9-slim

RUN useradd -m myuser && chown myuser:myuser /app
USER myuser
WORKDIR /app

COPY requirements.txt .
RUN python -m venv venv
RUN ./venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["./venv/bin/python", "app.py"]
"""
                (self.project_dir / file).write_text(content, encoding='utf-8')
                logging.info(f"Created {file} to fix deployment issues.")
            elif file == ".gitignore":
                content = """
.env
.env.*
__pycache__/
*.py[cod]
venv/
*.log
.vscode/
.idea/
node_modules/
*.local
"""
                (self.project_dir / file).write_text(content, encoding='utf-8')
                logging.info(f"Created {file} with sensitive file exclusions.")

    def _simulate_bot(self) -> None:
        """Simulate the chatbot's behavior, supporting English and Hebrew."""
        logging.info("Simulating Movne Chatbot behavior...")
        print("\n=== Movne Chatbot Simulation ===")
        print("Ask a question (type 'quit' to exit, 'he' for Hebrew responses):")
        
        while True:
            try:
                query = input("> ")
                if query.lower() in ['quit', 'exit']:
                    break
                    
                language = "he" if query.lower() == 'he' else "en"
                if language == "he":
                    print("שאלה (הקלד 'יציאה' לצאת):")
                    query = input("> ")
                    if query.lower() in ['יציאה', 'quit', 'exit']:
                        break
                
                if not self.openai_api_key:
                    raise ValueError("OpenAI API key is not set. Please check your environment variables or configuration.")
                
                response = self._query_openai(query, language)
                if language == "he":
                    print(f"תגובה: {response}")
                else:
                    print(f"Response: {response}")
                    
            except ValueError as ve:
                logging.error(f"Configuration error: {ve}")
                print(f"Error: {str(ve)}")
                break
            except Exception as e:
                logging.error(f"Bot simulation failed: {e}")
                error_msg = "שגיאה: לא ניתן לעבד את הבקשה. אנא בדוק את מפתח ה-API והחיבור." if language == "he" else \
                           "Error: Could not process your request. Please check the OpenAI API key and connection."
                print(error_msg)

    def _query_openai(self, query: str, language: str) -> str:
        """Query OpenAI API for chatbot responses, supporting English and Hebrew."""
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_api_key)
            
            # Prepare system message based on language
            system_message = {
                "role": "system",
                "content": "You are a helpful assistant. Please respond in Hebrew." if language == "he" else "You are a helpful assistant."
            }
            
            # Prepare messages for the API call
            messages = [system_message, {"role": "user", "content": query}]
            
            # Generate response using OpenAI
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")

    def _setup_environment(self) -> None:
        """Set up the environment variables and configuration files."""
        try:
            # Create or update .env file
            env_path = self.project_dir / '.env'
            env_content = f"OPENAI_API_KEY={self.openai_api_key}\nRAILWAY_PROJECT_ID={self.railway_project_id}\n"
            env_path.write_text(env_content, encoding='utf-8')
            logging.info("Environment variables set up successfully.")
            
            # Create or update railway.toml if it doesn't exist
            railway_config = self.project_dir / 'railway.toml'
            if not railway_config.exists():
                railway_content = f"[build]\nbuilder = \"nixpacks\"\nwatchPatterns = [\".env\", \"**/*.py\", \"requirements.txt\"]\n\n[deploy]\nstartCommand = \"python app.py\"\nhealthcheckPath = \"/health\"\nhealthcheckTimeout = 100\n"
                railway_config.write_text(railway_content, encoding='utf-8')
                logging.info("Railway configuration created successfully.")
        except Exception as e:
            logging.error(f"Failed to set up environment: {e}")
            raise

    def _ensure_gitignore(self) -> None:
        """Ensure .gitignore exists and contains necessary entries."""
        try:
            gitignore_path = self.project_dir / '.gitignore'
            if not gitignore_path.exists():
                gitignore_content = """.env
.env.*
__pycache__/
*.py[cod]
venv/
*.log
.vscode/
.idea/
node_modules/
*.local
"""
                gitignore_path.write_text(gitignore_content, encoding='utf-8')
                logging.info(".gitignore created with necessary exclusions.")
        except Exception as e:
            logging.error(f"Failed to create .gitignore: {e}")
            raise

    def _update_dockerfile(self) -> None:
        """Update Dockerfile with optimized configuration."""
        try:
            dockerfile_path = self.project_dir / 'Dockerfile'
            if dockerfile_path.exists():
                dockerfile_content = """
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m myuser && mkdir -p /app && chown myuser:myuser /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER myuser

# Set up Python environment
COPY requirements.txt .
RUN python -m venv venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["./venv/bin/python", "app.py"]
"""
                dockerfile_path.write_text(dockerfile_content, encoding='utf-8')
                logging.info("Dockerfile updated with optimized configuration.")
        except Exception as e:
            logging.error(f"Failed to update Dockerfile: {e}")
            raise

    def run(self) -> None:
        """Execute the complete deployment process."""
        try:
            # Step 1: Check prerequisites
            self._check_prerequisites()
            
            # Step 2: Ensure project structure
            self._ensure_project_structure()
            
            # Step 3: Set up environment
            self._setup_environment()
            
            # Step 4: Ensure .gitignore
            self._ensure_gitignore()
            
            # Step 5: Update Dockerfile
            self._update_dockerfile()
            
            # Step 6: Simulate bot for testing
            self._simulate_bot()
            
            logging.info("Deployment process completed successfully.")
            
        except Exception as e:
            logging.error(f"Deployment failed: {e}")
            raise

if __name__ == "__main__":
    # Example usage - replace with your actual credentials
    GITHUB_REPO = "https://github.com/aviadkim/movne-chatbot-v2.git"
    RAILWAY_PROJECT_ID = "6688ad4"  # Replace with your actual Railway project ID
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Use environment variable for security
    if not OPENAI_API_KEY:
        OPENAI_API_KEY = input("Please enter your OpenAI API key: ")
    
    agent = MovneChatbotAgent(GITHUB_REPO, RAILWAY_PROJECT_ID, OPENAI_API_KEY)
    agent.run()