#!/bin/bash

# Esperar a que la base de datos esté lista (si usaras Postgres)
echo "Waiting for database..."

# Ejecutar migraciones
echo "Running migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Crear superusuario si no existe (opcional)
# echo "Creating superuser..."
# python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

# Iniciar servidor
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000