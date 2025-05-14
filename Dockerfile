FROM python:3.9-slim  # Neutral (no menciona Debian explícitamente)

WORKDIR /app

# Instala solo dependencias esenciales (compatibles con cualquier host)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Fija versiones críticas
RUN pip install --upgrade "pip==20.3.4" "setuptools==59.6.0"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["rasa", "run", "--enable-api"]
