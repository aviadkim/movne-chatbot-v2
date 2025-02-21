
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m myuser && mkdir -p /app && chown myuser:myuser /app
WORKDIR /app

# Install system dependencies
RUN apt-get update &&     apt-get install -y --no-install-recommends git &&     apt-get clean &&     rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER myuser

# Set up Python environment
COPY requirements.txt .
RUN python -m venv venv &&     ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["./venv/bin/python", "app.py"]
