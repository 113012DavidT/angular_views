from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['JSON_SORT_KEYS'] = False

# Permitir CORS para todos los orígenes y exponer headers comunes
CORS(app, 
     resources={r"/api/*": {"origins": "*"}}, 
     supports_credentials=True, 
     expose_headers=["Content-Type", "Authorization"],
     allow_headers=["Content-Type", "Authorization"])

# Obtener puerto del entorno (Render usa PORT)
PORT = int(os.getenv('PORT', 5000))

def get_db_connection():
    """Crear conexión a la base de datos SQLite"""
    db_path = os.getenv('DATABASE_PATH', 'database.db')
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/login', methods=['POST', 'OPTIONS'])
def login():
    """Endpoint de autenticación"""
    # Manejar CORS preflight
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'Request body vacío'
            }), 400
            
        username = data.get('username')
        password = data.get('password')
        logger.info(f"🔐 LOGIN ATTEMPT: username='{username}'")
        
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
        
        if user:
            # Generar token JWT
            token = jwt.encode({
                'user_id': user['id'],
                'username': user['username'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, app.config['SECRET_KEY'], algorithm='HS256')
            
            logger.info(f"✓ LOGIN SUCCESS: user={user['username']}")
            return jsonify({
                'success': True,
                'token': token,
                'user': {
                    'id': user['id'],
                    'username': user['username']
                }
            }), 200
        else:
            logger.warning(f"✗ LOGIN FAILED: invalid credentials for {username}")
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
            
    except Exception as e:
        logger.error(f"❌ LOGIN ERROR: {str(e)}")
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
    logger.info("🚀 Iniciando servidor Flask")
    logger.info(f"📊 Puerto: {PORT}")
    logger.info("📊 Endpoints disponibles:")
    logger.info("   - POST /api/login")
    logger.info("   - GET  /api/esp32/data")
    logger.info("   - POST /api/esp32/data")
    logger.info("   - GET  /api/health")
    
    # En desarrollo: debug=True, en producción: debug=False
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=PORT)
