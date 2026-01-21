#!/usr/bin/env bash
# Esto detiene el proceso si algo sale mal
set -o errexit

# 1. Instala todas las librerías de tu requirements.txt
pip install -r requirements.txt

# 2. Prepara los archivos visuales (CSS, imágenes) para que se vean en internet
python manage.py collectstatic --no-input

# 3. Actualiza la base de datos con tus modelos de Django
python manage.py migrate