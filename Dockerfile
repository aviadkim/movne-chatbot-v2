# Build frontend
FROM node:18-alpine as frontend
WORKDIR /app/frontend

# Install dependencies with legacy peer deps and clean npm cache
COPY frontend/package*.json ./
RUN npm cache clean --force && \
    npm install --legacy-peer-deps --no-package-lock

# Build frontend
COPY frontend/ ./
RUN npm run build

# Build backend
FROM python:3.11-slim
WORKDIR /app

# Copy frontend build
COPY --from=frontend /app/frontend/build /app/static

# Install backend dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ /app/backend/

# Copy entry script
COPY start.sh .
RUN chmod +x start.sh

EXPOSE 8000
CMD ["./start.sh"]
