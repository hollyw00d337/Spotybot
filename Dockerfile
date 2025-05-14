# ¡IMPORTANTE! Usa esta imagen base específica
FROM python:3.9.18-slim-buster

WORKDIR /app

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# ¡CRÍTICO! Fija versiones ANTES de instalar dependencias
RUN pip install --upgrade "pip==20.3.4" "setuptools==59.6.0" "wheel==0.37.1"

COPY requirements.txt .

# Instala PyYAML desde fuente sin usar wheels
RUN pip install --no-cache-dir --no-binary :all: -r requirements.txt

COPY . .

CMD ["rasa", "run", "--enable-api"]
