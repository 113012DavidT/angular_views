#!/bin/bash
# Script de inicialización para Render

echo "🔧 Inicializando aplicación..."

# Cambiar al directorio del backend
cd backend || exit 1

# Inicializar la base de datos
echo "📊 Inicializando base de datos..."
python init_db.py

# Iniciar la aplicación
echo "🚀 Iniciando Flask con Gunicorn..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
