# Usa una imagen base de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala las dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copia el resto del código fuente
COPY . .

# Comando para ejecutar el bot
CMD ["python", "bot.py"]
