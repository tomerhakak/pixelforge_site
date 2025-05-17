# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
# Copy aircrack-ng and its dependencies first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Expose port 8000 for Django development server (or your production server port)
EXPOSE 8000

# Command to run the application (replace with your production server command, e.g., gunicorn)
# For now, using runserver for simplicity. Ensure DEBUG is False in production.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 