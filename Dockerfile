# Usa la imagen oficial de Rasa 3.6.2 (Python 3.8 embebido)
FROM rasa/rasa:3.6.2-full

# --- Configuración segura ---
USER root

#Instala dependencias del sistema SOLO si son necesarias
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

#Copia selectiva de archivos (evita sobrescribir dependencias existentes)
COPY data /app/data
COPY actions /app/actions
COPY config.yml /app/
COPY domain.yml /app/
COPY endpoints.yml /app/


# --- Vuelve al usuario no-root ---
USER 1001

# Puerto expuesto
EXPOSE 5005

# Comando de inicio (ajusta según necesidades)
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
