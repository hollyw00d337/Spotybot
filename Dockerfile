# Usa una imagen base compatible
FROM python:3.9.22-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema necesarias para Rasa y ciencia de datos
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    python3-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia el archivo de dependencias primero para aprovechar el cache
COPY requirements.txt .

# Actualiza pip y setuptools, luego instala dependencias de Python
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copia el resto del repositorio
COPY . .

# Expone el puerto
EXPOSE 5005

# Comando por defecto para correr el bot
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
