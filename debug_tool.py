import sys
import subprocess
import os
import logging
import requests
from pathlib import Path
import importlib
import pkg_resources

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

class SystemDebugger:
    def __init__(self):
        self.project_root = Path.cwd()
        self.backend_dir = self.project_root / 'backend'
        self.frontend_dir = self.project_root / 'frontend'
        self.errors = []
        self.warnings = []

    def check_python_dependencies(self):
        """בדיקת תלויות Python"""
        logger.info("Checking Python dependencies...")
        requirements_file = self.backend_dir / 'requirements.txt'
        
        try:
            with open(requirements_file) as f:
                requirements = pkg_resources.parse_requirements(f)
                for req in requirements:
                    try:
                        pkg_resources.require(str(req))
                        logger.info(f"✓ {req} installed correctly")
                    except Exception as e:
                        self.errors.append(f"Missing or incorrect package: {req}")
                        logger.error(f"✗ {req} - {str(e)}")
        except Exception as e:
            self.errors.append(f"Failed to read requirements.txt: {str(e)}")

    def check_node_dependencies(self):
        """בדיקת תלויות Node.js"""
        logger.info("Checking Node.js dependencies...")
        package_json = self.frontend_dir / 'package.json'
        
        try:
            if not os.path.exists(self.frontend_dir / 'node_modules'):
                self.warnings.append("node_modules directory not found")
            
            result = subprocess.run(['npm', 'list'], 
                                 cwd=self.frontend_dir, 
                                 capture_output=True, 
                                 text=True)
            if result.returncode != 0:
                self.warnings.append("Some npm packages might be missing")
        except Exception as e:
            self.errors.append(f"Failed to check npm dependencies: {str(e)}")

    def check_file_structure(self):
        """בדיקת מבנה הקבצים"""
        logger.info("Checking file structure...")
        required_files = [
            'backend/app/main.py',
            'backend/app/core/config.py',
            'backend/requirements.txt',
            'frontend/src/App.jsx',
            'frontend/src/index.js',
            'frontend/package.json',
            '.env.example',
            'docker-compose.yml'
        ]
        
        for file_path in required_files:
            full_path = self.project_root / file_path
            if not full_path.exists():
                self.errors.append(f"Missing required file: {file_path}")
            else:
                logger.info(f"✓ Found {file_path}")

    def check_env_variables(self):
        """בדיקת משתני סביבה"""
        logger.info("Checking environment variables...")
        required_vars = [
            'OPENAI_API_KEY',
            'POSTGRES_USER',
            'POSTGRES_PASSWORD',
            'POSTGRES_DB'
        ]
        
        for var in required_vars:
            if not os.getenv(var):
                self.warnings.append(f"Missing environment variable: {var}")

    def check_database_connection(self):
        """בדיקת חיבור למסד הנתונים"""
        logger.info("Checking database connection...")
        try:
            from backend.app.db.session import test_connection
            if test_connection():
                logger.info("✓ Database connection successful")
            else:
                self.errors.append("Database connection failed")
        except Exception as e:
            self.errors.append(f"Database connection error: {str(e)}")

    def run_backend_tests(self):
        """הרצת בדיקות Backend"""
        logger.info("Running backend tests...")
        try:
            result = subprocess.run(['pytest'], 
                                 cwd=self.backend_dir, 
                                 capture_output=True, 
                                 text=True)
            if result.returncode == 0:
                logger.info("✓ Backend tests passed")
            else:
                self.errors.append("Backend tests failed")
                logger.error(result.stdout)
        except Exception as e:
            self.errors.append(f"Failed to run backend tests: {str(e)}")

    def generate_report(self):
        """יצירת דוח בדיקה"""
        logger.info("Generating debug report...")
        report = {
            'errors': self.errors,
            'warnings': self.warnings,
            'status': 'FAIL' if self.errors else 'WARNING' if self.warnings else 'PASS'
        }
        
        with open('debug_report.txt', 'w') as f:
            f.write("=== Debug Report ===\n\n")
            f.write(f"Status: {report['status']}\n\n")
            
            if report['errors']:
                f.write("Errors:\n")
                for error in report['errors']:
                    f.write(f"- {error}\n")
            
            if report['warnings']:
                f.write("\nWarnings:\n")
                for warning in report['warnings']:
                    f.write(f"- {warning}\n")

        return report

    def run_all_checks(self):
        """הרצת כל הבדיקות"""
        self.check_python_dependencies()
        self.check_node_dependencies()
        self.check_file_structure()
        self.check_env_variables()
        self.run_backend_tests()
        self.check_database_connection()
        return self.generate_report()

if __name__ == "__main__":
    debugger = SystemDebugger()
    report = debugger.run_all_checks()
    print(f"\nDebug completed with status: {report['status']}")
