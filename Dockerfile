# Dockerfile for Django + Tailwind
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements (if exists) and install
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Copy project
COPY ./app /app

# Install Tailwind dependencies (if needed)
RUN if [ -f manage.py ]; then python manage.py tailwind install; fi

# Expose port
EXPOSE 8000

# Default command
CMD ["sh", "-c", "python manage.py migrate && python manage.py tailwind build && python manage.py runserver 0.0.0.0:8000"]
