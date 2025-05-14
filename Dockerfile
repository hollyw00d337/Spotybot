# Usa una imagen base con Python 3.10
FROM python:3.10-slim

# Actualiza los paquetes e instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Crea y define el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala Rasa
RUN pip install --upgrade pip && pip install rasa

# Puerto expuesto por Rasa
EXPOSE 5005

# Comando por defecto al ejecutar el contenedor
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]
