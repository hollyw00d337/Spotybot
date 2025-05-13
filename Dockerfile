# Imagen base con Python 3.11
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código fuente al contenedor
COPY . /app

# Instalar dependencias del sistema necesarias para Rasa
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Actualizar pip e instalar Rasa
RUN pip install --upgrade pip \
    && pip install rasa==3.1.1

# Entrenar el modelo de Rasa
RUN rasa train

# Exponer el puerto recomendado por Rasa
EXPOSE 5005

# Comando que se ejecutará al iniciar el contenedor
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
