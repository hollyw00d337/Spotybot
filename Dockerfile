# Usa la imagen oficial de Rasa 3.6.2 (TODO incluido)
FROM rasa/rasa:3.6.2-full

# Copia SOLO los archivos necesarios (evita duplicar dependencias)
COPY data /app/data
COPY actions /app/actions
COPY config.yml /app/
COPY domain.yml /app/
COPY credentials.yml /app/
COPY endpoints.yml /app/

USER 1001


EXPOSE 5005
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
