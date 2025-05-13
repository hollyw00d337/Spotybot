# Imagen base con Python 3.11
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código fuente al contenedor
COPY . /app

# Actualizar pip e instalar Rasa
RUN pip install --upgrade pip \
    && pip install rasa==3.1.1

# Entrenar el modelo de Rasa
RUN rasa train

# Exponer el puerto recomendado por Rasa
EXPOSE 5005

# Comando que se ejecutará al iniciar el contenedor
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
