# Usa una imagen base de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Evita que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Asegura que el stdout/stderr no esté bufferizado
ENV PYTHONUNBUFFERED=1

# Instala dependencias del sistema necesarias para compilar grpcio y otros paquetes
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
    curl \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libjpeg-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos de requerimientos
COPY requirements.txt .

# Actualiza pip y herramientas necesarias para construir paquetes
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu proyecto al contenedor
COPY . .

# Comando por defecto (
CMD ["rasa", "--help"]

