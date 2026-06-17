#!/bin/bash
# MIE Quick Start Script

echo ""
echo "╔══════════════════════════════════════╗"
echo "║   Market Intelligence Engine v1.0    ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Backend
echo "→ Starting Python backend..."
cd backend
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo "  ⚠  Created .env — add your GEMINI_API_KEY"
fi
pip install -r requirements.txt -q
python app.py &
BACKEND_PID=$!
echo "  ✓  Backend PID: $BACKEND_PID"

cd ..

# Frontend
echo ""
echo "→ Installing frontend dependencies..."
cd frontend
npm install --silent
echo "  ✓  Dependencies installed"
echo ""
echo "→ Starting React frontend..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "╔══════════════════════════════════════╗"
echo "║  Frontend: http://localhost:3000      ║"
echo "║  Backend:  http://localhost:4000      ║"
echo "║  Health:   http://localhost:4000/api/health"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
