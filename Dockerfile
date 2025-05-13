# Dockerfile, imagen base donde crearemos el contenedor, usando python 3.11 como version
FROM python:3.11-slim
#Copiar todo el codigo fuente de la repo
COPY . /app

#instala Rasa
RUN pip install --upgrade pip
RUN pip install rasa==3.11
#copiamos archivos del proyecto
COPY . /app
#Cambiamos el directorio usandolo como comando predeterminado
WORKDIR /app
# Entrenamos el modelo de Rasa
RUN rasa train

# Exponemos el puerto recomendado por Rasa
EXPOSE 5005
#Comando que se ejecutara al inicial el contenedor
CMD ["run", "--enable-api", "--cors", "*"]
