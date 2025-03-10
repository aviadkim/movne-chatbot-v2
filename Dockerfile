
FROM python:3.11-slim

# Create a non-root user
RUN useradd -m myuser && mkdir -p /app && chown myuser:myuser /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY --chown=myuser:myuser backend/requirements.txt requirements.txt

# Switch to non-root user
USER myuser

# Set up Python environment
RUN python -m venv venv && \
    ./venv/bin/pip install --no-cache-dir wheel && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=myuser:myuser . .

# Expose the port the app runs on
EXPOSE ${PORT}

# Command to run the application
CMD ["./venv/bin/python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
