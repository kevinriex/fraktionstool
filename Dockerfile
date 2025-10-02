# --- Stage 1: Node/Tailwind Build ---
FROM node:20-slim as frontend

WORKDIR /frontend

# Falls du ein package.json für Tailwind/JS hast:
COPY ./app/package*.json ./
RUN npm install

# Copy restliches Projekt (für Tailwind Config etc.)
COPY ./app ./

# Baue Tailwind (CSS wird in /frontend/static oder wo du's definierst generiert)
RUN npm run build || echo "Kein build script definiert"


# --- Stage 2: Python Backend ---
FROM python:3.13-slim as backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System-Dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies
COPY ./app/requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Kopiere Django-Projekt
COPY ./app /app

# --- Wichtiger Teil: Kopiere nur die fertigen Assets von Stage 1 ---
COPY --from=frontend /frontend/static /app/static

# Expose Port
EXPOSE 8000

# Startkommando
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
