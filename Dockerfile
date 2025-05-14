FROM python:3.9.22-slim

WORKDIR /app

# Instala dependencias del sistema (evita paquetes innecesarios)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Fija versiones ANTIGUAS de pip/setuptools antes de instalar dependencias
RUN pip install --upgrade "pip==21.3.1" "setuptools==59.6.0" "wheel==0.37.1"

COPY requirements.txt .

# Instala dependencias con --no-deps para evitar conflictos
RUN pip install --no-cache-dir --no-deps -r requirements.txt

COPY . .

EXPOSE 5005

CMD ["rasa", "run", "--enable-api", "--cors", "*"]
