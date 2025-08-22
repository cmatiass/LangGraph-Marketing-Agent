#!/bin/bash
# Render build script - builds frontend and copies to backend

echo "🏗️ Building React frontend..."
cd frontend
npm ci
npm run build

echo "📁 Copying build to backend..."
mkdir -p ../backend/static
cp -r build/* ../backend/static/

echo "✅ Build complete!"
