#!/bin/bash

# Kill background processes on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

echo "Starting WalletGenie Locally..."

# Start Backend
echo "Starting Backend..."
cd backend
# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Run FastAPI
uvicorn main:app --reload --port 8080 &
BACKEND_PID=$!
cd ..

# Start Frontend
echo "Starting Frontend..."
cd frontend
# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

ng serve --port 4200 &
FRONTEND_PID=$!
cd ..

echo "Backend running at http://localhost:8080"
echo "Frontend running at http://localhost:4200"
echo "Press CTRL+C to stop."

wait
