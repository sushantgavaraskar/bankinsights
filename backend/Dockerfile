# Base image with Python
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Environment variables (in production use Docker secrets or .env)
ENV DJANGO_SETTINGS_MODULE=bankinsight_backend.settings

# Run with Gunicorn
CMD ["gunicorn", "bankinsight_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
