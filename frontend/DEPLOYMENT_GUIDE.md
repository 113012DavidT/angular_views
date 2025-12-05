# ESP32 Telemetry PWA Dashboard

Aplicación Angular PWA para monitorear datos de sensores ESP32 en tiempo real con login y dashboard responsivo.

## 📱 Características

- **Progressive Web App (PWA)** - Instalable en dispositivos móviles
- **Login Seguro** - Autenticación con JWT y SQLite
- **Dashboard Responsivo** - Optimizado para móvil y desktop
- **Telemetría en Tiempo Real** - Datos del sensor actualizados cada 5 segundos
- **Historial de Datos** - Tabla con timestamps y intervalos de transmisión
- **Offline Support** - Funciona parcialmente sin conexión

## 🛠️ Stack Técnico

### Frontend
- **Angular 21** - Framework principal
- **Tailwind CSS 4.1** - Estilos responsivos
- **PrimeNG 20.3** - Componentes UI
- **RxJS** - Manejo de observables
- **Service Worker** - Soporte offline

### Backend
- **Servidor de Telemetría:** Express + MongoDB (Render)
  - URL: `https://esp32-server-9ip3.onrender.com/api/telemetry`
- **Servidor de Autenticación:** Flask + SQLite (Local)
  - Puerto: `localhost:5000`

## 📋 Requisitos Previos

- Node.js >= 18
- npm >= 9
- Angular CLI >= 17
- Python 3.8+ (para backend local)

## 🚀 Instalación Local

### Frontend

```bash
cd frontend
npm install
npm start
```

La aplicación estará disponible en `http://localhost:4200`

### Backend (Opcional - Solo para autenticación local)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

El backend estará en `http://localhost:5000`

## 🔐 Credenciales de Prueba

```
Usuario: admin
Contraseña: admin123
```

## 📊 API Endpoints

### Telemetría (Render)
- **GET** `/api/telemetry` - Obtener últimas 50 lecturas
- **GET** `/api/telemetry/last` - Obtener último dato
- **GET** `/api/telemetry/count` - Contar registros totales

### Autenticación (Local)
- **POST** `/api/login` - Login con credenciales

**Payload:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Respuesta:**
```json
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com"
  }
}
```

## 🌍 Variables de Entorno

### Frontend (`.env`)
```env
NG_APP_API_AUTH=http://localhost:5000/api
NG_APP_API_TELEMETRY=https://esp32-server-9ip3.onrender.com/api
```

### Backend (`.env`)
```env
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
CORS_ORIGINS=http://localhost:4200,http://localhost:3000
```

## 📦 Estructura del Proyecto

```
angular_views/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── auth/
│   │   │   │   ├── auth.ts (AuthService)
│   │   │   │   └── login/ (Login Component)
│   │   │   ├── dashboard/
│   │   │   │   ├── dashboard.ts (Dashboard Component)
│   │   │   │   └── dashboard.html
│   │   │   ├── services/
│   │   │   │   └── telemetry.service.ts
│   │   │   ├── guards/
│   │   │   │   └── auth.guard.ts
│   │   │   └── app.routes.ts
│   │   ├── main.ts
│   │   ├── manifest.webmanifest
│   │   └── styles.scss
│   ├── angular.json
│   ├── tailwind.config.js
│   ├── vercel.json
│   └── package.json
├── backend/
│   ├── app.py
│   ├── init_db.py
│   ├── requirements.txt
│   └── .env
└── README.md
```

## 🔄 Flujo de Datos

```
ESP32 (Sensor)
    ↓
    POST /api/telemetry (Render)
    ↓
MongoDB (Render)
    ↓
    GET /api/telemetry (Frontend)
    ↓
Dashboard (Angular PWA)
```

## 📈 Tabla de Telemetría

La tabla muestra:
- **Hora ESP32**: Timestamp del sensor (México)
- **Recibido**: Cuando el servidor recibió el dato
- **Guardado**: Cuando se guardó en MongoDB
- **Intervalo**: Segundos desde la última lectura (color-coded)
  - 🟢 Verde: Normal (< 60s)
  - 🟡 Amarillo: Lento (60-120s)
  - 🔴 Rojo: Muy lento (> 120s)
- **Temperatura** y **Humedad**: Valores actuales

## 🚢 Despliegue en Vercel

1. **Conectar repositorio:**
   - Ve a https://vercel.com
   - Importa tu repositorio de GitHub
   - Selecciona `angular_views`

2. **Configurar build:**
   - Framework: `Angular`
   - Build Command: `npm run build`
   - Output Directory: `dist/app-esp/browser`

3. **Variables de entorno:**
   - `API_TELEMETRY_URL`: `https://esp32-server-9ip3.onrender.com`

4. **Deploy:**
   - Vercel desplegará automáticamente en cada push a `main`

### URL de Producción
```
https://angular-views-beta.vercel.app
```

## 🔍 Debugging

### Ver logs del servicio de telemetría
```typescript
// En el navegador - F12 Console
localStorage.getItem('token') // Verificar JWT
```

### Test de API
```bash
# Obtener último dato
curl https://esp32-server-9ip3.onrender.com/api/telemetry/last

# Obtener historial
curl https://esp32-server-9ip3.onrender.com/api/telemetry
```

## 📱 Instalación como PWA

1. En navegador, haz clic en el icono de "Instalar" (dirección o app drawer)
2. O vía menú: Chrome → Menú → "Instalar app"
3. La PWA se ejecutará en modo offline (datos cacheados)

## ⚠️ Troubleshooting

### "No hay datos"
- Verifica que el ESP32 esté enviando datos a Render
- Abre DevTools (F12) → Network → /api/telemetry
- Comprueba CORS en backend

### "Login fallido"
- Asegúrate de que Flask esté corriendo en localhost:5000
- Verifica credenciales (admin/admin123)
- Reinicia la base de datos: `python init_db.py`

### "PWA no se instala"
- Usa HTTPS en producción (Vercel proporciona)
- El service worker debe estar registrado
- Verifica en DevTools → Application → Service Workers

## 🤝 Contribuir

Para hacer cambios:
1. Crea una rama: `git checkout -b feature/tu-feature`
2. Haz commit: `git commit -am 'Agregar feature'`
3. Push: `git push origin feature/tu-feature`
4. Pull Request

## 📝 Licencia

MIT - Libre para usar y modificar

## 👤 Autor

David Torres

## 📞 Soporte

Para issues o preguntas, crea un issue en GitHub:
https://github.com/113012DavidT/angular_views/issues

---

**Última actualización**: Diciembre 2025
