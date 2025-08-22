# Render.com deployment configuration for LangGraph Marketing Agent
# This file configures the build process for the unified backend+frontend deployment

# Build Command:
cd frontend && npm install && npm run build && cp -r build/* ../backend/static/

# Start Command:
cd backend && pip install -r requirements.txt && uvicorn main:app --host=0.0.0.0 --port=$PORT

# Environment Variables needed:
# - OPENAI_API_KEY: Your OpenAI API key for GPT-4
# - PORT: Automatically provided by Render

# Pre-Deploy Command (Optional):
# rm -rf backend/static/* (to clean old builds)

# Notes:
# - Root Directory: leave empty (use repository root)
# - The app will be available on the URL provided by Render
# - Both API and React frontend will be served from the same URL
# - API endpoints: /api/*, /health, /ws/*
# - Frontend: all other routes serve the React app
