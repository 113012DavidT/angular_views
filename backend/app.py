from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
# Permitir CORS para todos los orígenes y exponer headers comunes
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, expose_headers=["Content-Type", "Authorization"])

def get_db_connection():
    """Crear conexión a la base de datos SQLite"""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint de autenticación"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        print(f"🔐 LOGIN ATTEMPT: username='{username}', password='{password}'")
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Usuario y contraseña requeridos'
            }), 400
        
        conn = get_db_connection()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?',
            (username, password)
        ).fetchone()
        conn.close()
        
        print(f"✓ DB QUERY RESULT: user={dict(user) if user else 'NOT FOUND'}")
        
        if user:
            # Generar token JWT
            token = jwt.encode({
                'user_id': user['id'],
                'username': user['username'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error en el servidor: {str(e)}'
        }), 500

@app.route('/api/esp32/data', methods=['GET'])
def get_esp32_data():
    """Obtener últimos datos del ESP32"""
    try:
        conn = get_db_connection()
        data = conn.execute(
            'SELECT * FROM esp32_data ORDER BY timestamp DESC LIMIT 10'
        ).fetchall()
        conn.close()
        
        return jsonify({
            'success': True,
            'data': [dict(row) for row in data]
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/esp32/data', methods=['POST'])
def save_esp32_data():
    """Guardar datos del ESP32 (endpoint para el ESP32)"""
    try:
        data = request.get_json()
        temperature = data.get('temperature')
        humidity = data.get('humidity')
        status = data.get('status', 'active')
        
        conn = get_db_connection()
        conn.execute(
            'INSERT INTO esp32_data (temperature, humidity, status) VALUES (?, ?, ?)',
            (temperature, humidity, status)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Datos guardados correctamente'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'API funcionando correctamente'
    }), 200

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask en http://localhost:5000")
    print("📊 Endpoints disponibles:")
    print("   - POST /api/login")
    print("   - GET  /api/esp32/data")
    print("   - POST /api/esp32/data")
    print("   - GET  /api/health")
    app.run(debug=True, host='0.0.0.0', port=5000)
