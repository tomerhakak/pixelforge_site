#!/bin/bash

# Try to kill existing process on port 8001
echo "Attempting to free port 8001..."
kill $(lsof -t -i:8001) 2>/dev/null || true

# Run backend server
echo "Starting Django backend server..."
cd backend
source venv/bin/activate
python manage.py runserver 8001 &
BACKEND_PID=$!

# Try to kill existing process on port 8080
echo "Attempting to free port 8080..."
kill $(lsof -t -i:8080) 2>/dev/null || true

# Run frontend server
echo "Starting Flutter frontend server..."
cd ../frontend
flutter run -d web-server --web-port 8080 &
FRONTEND_PID=$!

# Function to kill processes on exit
function cleanup {
  echo "Stopping servers..."
  kill $BACKEND_PID $FRONTEND_PID
}

# Register the cleanup function for when script exits
trap cleanup EXIT

# Keep script running
echo "Both servers are running. Press Ctrl+C to stop."
wait 