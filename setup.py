from setuptools import setup, find_packages

setup(
    name="movne-chatbot",
    version="3.1.0",
    packages=find_packages(),
    install_requires=[
        line.strip()
        for line in open("backend/requirements.txt")
        if line.strip() and not line.startswith("#")
    ],
    python_requires=">=3.11",
)
