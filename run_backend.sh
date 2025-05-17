#!/bin/bash

# Run backend server on port 8001
echo "Starting Django backend server on port 8001..."
cd backend
source venv/bin/activate
python manage.py runserver 8001

echo "Backend server stopped." 