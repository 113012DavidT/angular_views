import sqlite3
from datetime import datetime

def init_db():
    """Inicializar la base de datos SQLite con las tablas necesarias"""
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de datos ESP32 (para uso futuro)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS esp32_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            status TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertar usuarios de prueba (password: admin123 y pruebas123)
    # En producción usar hash apropiado
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email)
        VALUES ('admin', 'admin123', 'admin@example.com')
    ''')
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, email)
        VALUES ('pruebas', 'pruebas123', 'pruebas@example.com')
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_db()
