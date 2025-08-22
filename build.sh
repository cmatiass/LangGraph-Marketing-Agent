#!/bin/bash
# Build script para compilar el frontend React y copiarlo al backend

echo "🏗️  Building React Frontend for Production..."

# Navigate to frontend directory
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Build React app
echo "⚛️  Building React app..."
npm run build

# Check if build succeeded
if [ $? -eq 0 ]; then
    echo "✅ Frontend build successful!"
    
    # Create backend static directory if it doesn't exist
    mkdir -p ../backend/static
    
    # Copy build files to backend static directory
    echo "📁 Copying build files to backend..."
    cp -r build/* ../backend/static/
    
    echo "🎉 Frontend successfully built and copied to backend!"
    echo "📂 Files copied to: backend/static/"
    echo ""
    echo "Now you can run the backend with:"
    echo "cd backend && python main.py"
    echo ""
    echo "The app will be available at: http://localhost:8000"
else
    echo "❌ Frontend build failed!"
    exit 1
fi
