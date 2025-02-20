import os
import subprocess
import sys
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    requirements_file = Path("backend/requirements.txt")
    if not requirements_file.exists():
        print("Error: requirements.txt not found")
        return False
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error installing dependencies")
        return False

def test_docker_build():
    """Test if Docker image can be built locally"""
    print("Testing Docker build...")
    try:
        subprocess.run(["docker", "build", "-t", "movne-chatbot-test", "."], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Error building Docker image")
        return False
    except FileNotFoundError:
        print("Docker not found. Please install Docker to test container builds.")
        return False

def test_environment_variables():
    """Check if all required environment variables are set"""
    print("Checking environment variables...")
    required_vars = [
        "HUGGINGFACE_TOKEN",
        "SECRET_KEY",
        "OLLAMA_HOST",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
        "POSTGRES_SERVER"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    return True

def run_tests():
    """Run the test suite"""
    print("Running tests...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "backend"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("Tests failed")
        return False

def main():
    print("=== Local Deployment Test ===")
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Environment Variables", test_environment_variables),
        ("Tests", run_tests),
        ("Docker Build", test_docker_build)
    ]
    
    results = []
    for name, check in checks:
        print(f"\n{name} Check:")
        result = check()
        results.append((name, result))
        print(f"{name}: {'✓ Passed' if result else '✗ Failed'}")
    
    print("\n=== Summary ===")
    all_passed = all(result for _, result in results)
    for name, result in results:
        print(f"{name}: {'✓ Passed' if result else '✗ Failed'}")
    
    if all_passed:
        print("\n✓ All checks passed! Ready for deployment.")
    else:
        print("\n✗ Some checks failed. Please fix the issues before deploying.")

if __name__ == "__main__":
    main()