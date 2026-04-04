FROM python:3.11-slim

# Evita archivos basura y muestra logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Carpeta de trabajo
WORKDIR /app

# Instalación de herramientas de sistema para la base de datos
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalación de librerías de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del asistente
COPY . /app/

# Arrancar el motor Gunicorn
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:10000"]