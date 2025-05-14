# Usa la imagen oficial de Rasa con todo incluido
FROM rasa/rasa:3.6.2-full

# Copia tus archivos al directorio estándar de Rasa (/app)
COPY . /app

# Puerto expuesto (para la API de Rasa)
EXPOSE 5005

# Comando para iniciar Rasa
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
