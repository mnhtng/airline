#!/bin/bash

echo "🚀 Starting deployment..."

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Backend
echo "🐍 Updating backend..."
cd backend
source .venv/bin/activate
pip install -r requirements.txt
deactivate
cd ..

# Restart backend service
echo "♻️ Restarting backend service..."
sudo systemctl restart airline-backend

# Frontend
echo "🌐 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Restart Nginx
echo "♻️ Restarting Nginx..."
sudo systemctl restart nginx

echo "✅ Deployment completed!"