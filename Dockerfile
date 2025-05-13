# Dockerfile, imagen base donde crearemos el contenedor, usando python 3.11 como version
FROM rasa/rasa:3.11
#Copiar todo el codigo fuente de la repo
COPY . /app
#Cambiamos el directorio usandolo como comando predeterminado
WORKDIR /app

# Entrenamos el modelo de Rasa
RUN rasa train

# Exponemos el puerto recomendado por Rasa
EXPOSE 5005
#Comando que se ejecutara al inicial el contenedor
CMD ["run", "--enable-api", "--cors", "*"]
