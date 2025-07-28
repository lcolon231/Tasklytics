#!/usr/bin/env bash

echo "📦 Installing frontend deps & building Vite app..."
cd frontend
npm install
npm run build

echo "🚀 Starting FastAPI server..."
cd ..
uvicorn app.main:app --host 0.0.0.0 --port 10000
