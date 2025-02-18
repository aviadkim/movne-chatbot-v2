import sys
import logging
import requests
import subprocess
from pathlib import Path
import pkg_resources
import docker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_dependencies():
    logger.info("Checking Python dependencies...")
    required = [
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
        'pydantic>=1.8.0',
        'pydantic-settings>=2.0.0',
        'python-dotenv>=0.19.0',
        'sqlalchemy>=1.4.23',
        'psycopg2-binary>=2.9.1',
        'alembic>=1.7.3',
        'chromadb>=0.4.15',
        'sentence-transformers>=2.2.2',
        'pytest>=7.0.0',
        'httpx>=0.25.0'
    ]
    
    for package in required:
        try:
            pkg_resources.require(package)
            logger.info(f"✓ {package} installed correctly")
        except Exception as e:
            logger.error(f"✗ {package} issue: {str(e)}")

def check_docker_services():
    logger.info("Checking Docker services...")
    client = docker.from_env()
    required_services = ['backend', 'frontend', 'db', 'ollama']
    
    try:
        containers = client.containers.list()
        running_services = [container.name for container in containers]
        
        for service in required_services:
            if any(service in container for container in running_services):
                logger.info(f"✓ {service} is running")
            else:
                logger.error(f"✗ {service} is not running")
    except Exception as e:
        logger.error(f"Docker check failed: {str(e)}")

def check_file_structure():
    logger.info("Checking file structure...")
    required_files = [
        'backend/app/main.py',
        'backend/app/core/config.py',
        'backend/requirements.txt',
        'frontend/src/App.jsx',
        'frontend/src/index.js',
        'frontend/package.json',
        '.env',
        'docker-compose.yml',
        'frontend/Dockerfile',
        'backend/Dockerfile'
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            logger.info(f"✓ Found {file_path}")
        else:
            logger.error(f"✗ Missing {file_path}")

def check_ollama_service():
    logger.info("Checking Ollama service...")
    try:
        response = requests.get("http://localhost:11434/api/version")
        if response.status_code == 200:
            logger.info("✓ Ollama service is responding")
        else:
            logger.error("✗ Ollama service returned unexpected status code")
    except requests.exceptions.RequestException:
        logger.error("✗ Ollama service is not accessible")

def check_env_variables():
    logger.info("Checking environment variables...")
    required_vars = [
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_DB',
        'DATABASE_URL',
        'SECRET_KEY'
    ]
    
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    for var in required_vars:
        if os.getenv(var):
            logger.info(f"✓ {var} is set")
        else:
            logger.error(f"✗ {var} is not set")

def run_backend_tests():
    logger.info("Running backend tests...")
    try:
        result = subprocess.run(
            ['pytest', 'backend'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(result.stderr)
    except Exception as e:
        logger.error(f"Failed to run tests: {str(e)}")

def main():
    try:
        check_python_dependencies()
        check_docker_services()
        check_file_structure()
        check_ollama_service()
        check_env_variables()
        run_backend_tests()
        
        logger.info("Generating debug report...")
        return 0
    except Exception as e:
        logger.error(f"Debug failed: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
