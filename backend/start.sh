#!/bin/bash

# Script para iniciar la aplicación Flask en Render
echo "🚀 Iniciando aplicación..."
echo "📍 Directorio actual: $(pwd)"
echo "📁 Contenido de directorio:"
ls -la

# Inicializar base de datos
echo "📊 Inicializando base de datos..."
python init_db.py

# Verificar que la BD fue creada
if [ -f "database.db" ]; then
    echo "✅ database.db creada exitosamente"
    ls -lh database.db
else
    echo "⚠️ database.db NO fue creada"
fi

# Ejecutar Gunicorn
echo "🌐 Iniciando Gunicorn..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --access-logfile - --error-logfile -
