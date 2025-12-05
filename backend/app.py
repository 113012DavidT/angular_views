from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import logging
import sys

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
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

# Ruta de la BD
DB_PATH = os.getenv('DATABASE_PATH', 'database.db')

def init_database():
    """Inicializar la base de datos si no existe"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Crear tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla de datos ESP32
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS esp32_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperature REAL,
                humidity REAL,
                status TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insertar usuario de prueba
        cursor.execute('''
            INSERT OR IGNORE INTO users (username, password, email)
            VALUES ('admin', 'admin123', 'admin@example.com')
        ''')
        
        conn.commit()
        conn.close()
        logger.info("✅ Base de datos inicializada correctamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error inicializando BD: {str(e)}")
        return False

def get_db_connection():
    """Crear conexión a la base de datos SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"❌ Error conectando a BD: {str(e)}")
        return None

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
