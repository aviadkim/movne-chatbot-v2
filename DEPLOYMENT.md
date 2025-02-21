# Deployment Guide for Movne Chatbot V2

## Prerequisites

1. Install the following tools:
   - Git
   - Node.js and npm
   - Python 3.11+
   - Railway CLI

2. Have accounts ready for:
   - GitHub
   - Railway
   - OpenAI (for API key)

## Deployment Steps

### 1. Initial Setup

```bash
# Clone the repository
git clone https://github.com/aviadkim/movne-chatbot-v2.git
cd movne-chatbot-v2

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

### 2. Environment Configuration

1. Create a `.env` file in the root directory:

```bash
# Create .env file
echo OPENAI_API_KEY=your_api_key > .env
echo ENVIRONMENT=production >> .env
echo PORT=8000 >> .env
echo POSTGRES_USER=postgres >> .env
echo POSTGRES_PASSWORD=your_password >> .env
echo POSTGRES_DB=movne >> .env
echo SECRET_KEY=your_secret_key >> .env
```

### 3. GitHub Deployment

```bash
# Initialize git repository (if not already done)
git init

# Add files to git
git add .

# Commit changes
git commit -m "Initial commit"

# Add remote repository
git remote add origin https://github.com/yourusername/movne-chatbot-v2.git

# Push to GitHub
git push -u origin main
```

### 4. Railway Deployment

```bash
# Login to Railway
railway login

# Initialize Railway project
railway init

# Link to existing project (if you already created one on Railway)
railway link

# Add environment variables to Railway
railway vars set OPENAI_API_KEY=your_api_key
railway vars set ENVIRONMENT=production
railway vars set PORT=8000
railway vars set POSTGRES_USER=postgres
railway vars set POSTGRES_PASSWORD=your_password
railway vars set POSTGRES_DB=movne
railway vars set SECRET_KEY=your_secret_key

# Deploy to Railway
railway up
```

### 5. Verify Deployment

1. Check GitHub repository to ensure all files are pushed
2. Visit your Railway dashboard to monitor the deployment
3. Once deployed, Railway will provide you with a URL where your application is hosted

## Important Notes

- Never commit the `.env` file to version control
- Keep your API keys and secrets secure
- Monitor your Railway dashboard for deployment status and logs
- Update environment variables in Railway dashboard as needed

## Troubleshooting

1. If deployment fails, check Railway logs for errors
2. Ensure all environment variables are properly set
3. Verify that all dependencies are properly listed in requirements.txt and package.json
4. Check if the PostgreSQL database is properly configured in Railway

## Maintenance

To update your deployment:

```bash
# Pull latest changes
git pull origin main

# Deploy updates
railway up
```