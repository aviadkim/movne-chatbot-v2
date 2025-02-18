import os
from pathlib import Path
import logging
import sys
import importlib

# הגדרת לוגר
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProjectChecker:
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.root = Path.cwd()

    def check_structure(self):
        """בדיקת מבנה הפרויקט"""
        required_dirs = [
            'backend/app/api/v1/endpoints',
            'backend/app/core',
            'backend/app/services',
            'backend/app/models',
            'frontend/src/components',
            'frontend/src/services'
        ]
        
        required_files = [
            'backend/requirements.txt',
            'backend/app/main.py',
            'backend/app/core/config.py',
            'backend/app/services/chat_service.py',
            'backend/app/services/rag_service.py',
            'frontend/package.json',
            '.env',
            'docker-compose.yml'
        ]

        for dir_path in required_dirs:
            if not (self.root / dir_path).exists():
                self.issues.append(f"Missing directory: {dir_path}")

        for file_path in required_files:
            if not (self.root / file_path).exists():
                self.issues.append(f"Missing file: {file_path}")

    def check_dependencies(self):
        """בדיקת תלויות Python"""
        required_packages = [
            'fastapi',
            'uvicorn',
            'pydantic',
            'sqlalchemy',
            'transformers',
            'torch',
            'faiss'
        ]
        
        for package in required_packages:
            try:
                if package == 'faiss':
                    import faiss
                else:
                    importlib.import_module(package)
                logger.info(f"✓ {package} installed correctly")
            except ImportError:
                self.issues.append(f"Missing package: {package}")

    def check_environment(self):
        """בדיקת משתני סביבה"""
        required_vars = [
            'POSTGRES_USER',
            'POSTGRES_PASSWORD',
            'POSTGRES_DB',
            'SECRET_KEY'
        ]
        
        for var in required_vars:
            if var not in os.environ:
                self.warnings.append(f"Missing environment variable: {var}")

    def check_main_imports(self):
        """בדיקת יבוא מודולים עיקריים"""
        try:
            sys.path.append(str(self.root / 'backend'))
            from app.services.chat_service import ChatService
            from app.services.rag_service import RAGService
            logger.info("✓ Main service imports successful")
        except Exception as e:
            self.issues.append(f"Import error: {str(e)}")

    def run_checks(self):
        """הרצת כל הבדיקות"""
        logger.info("Starting project checks...")
        
        self.check_structure()
        self.check_dependencies()
        self.check_environment()
        self.check_main_imports()
        
        print("\n=== Project Check Results ===")
        if self.issues:
            print("\nIssues Found:")
            for issue in self.issues:
                print(f"❌ {issue}")
        
        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"⚠️ {warning}")
            
        if not self.issues and not self.warnings:
            print("✅ All checks passed!")

        return len(self.issues) == 0

if __name__ == "__main__":
    checker = ProjectChecker()
    success = checker.run_checks()
    
    if not success:
        logger.error("Project check failed!")
        sys.exit(1)
    else:
        logger.info("Project check passed!")
