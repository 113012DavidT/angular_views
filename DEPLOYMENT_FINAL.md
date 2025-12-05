# 📋 PASOS FINALES PARA COMPLETAR EL DESPLIEGUE

## 🚀 Resumen Actual

Tienes **2 servicios** para desplegar:

| Servicio | Tipo | Estado |
|----------|------|--------|
| **Frontend** | Angular PWA (Vercel) | ✅ Listo |
| **Backend** | Flask Auth API (Render) | ✅ Listo |

---

## 📌 Orden de Despliegue RECOMENDADO

### 1️⃣ PRIMERO: Desplegar Backend en Render (10 min)

**Por qué primero?** Necesitas la URL del backend para configurar el frontend.

**Pasos:**

1. Ve a https://render.com
2. Haz click **"New +"** → **"Web Service"**
3. Selecciona **"Connect Repository"**
4. Busca y conecta `angular_views`
5. **Configuración:**
   - **Name:** `esp32-auth-api` (o tu nombre preferido)
   - **Environment:** Python 3
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && gunicorn app:app`

6. **Environment Variables:**
   ```
   SECRET_KEY = (genera algo aleatorio, ej: a7f3c9e1b2d4f6h8j0k2l4m6n8p0q2r4s6t8u0v2w4x6y8z0a2b4c6d8e0f2g4)
   FLASK_ENV = production
   ```

7. Click **"Create Web Service"**
8. Espera 5 minutos hasta que esté **"Live"** (verás luz verde)
9. Tu URL será algo como: `https://esp32-auth-api.onrender.com`
   - ✅ **GUARDA ESTA URL** (la necesitas en el siguiente paso)

**Verifica que funciona:**
```bash
curl https://tu-servicio.onrender.com/api/health
# Debe retornar: {"status": "ok", "message": "API funcionando correctamente"}
```

---

### 2️⃣ SEGUNDO: Actualizar Frontend con URL del Backend

Una vez tengas la URL del backend (ej: `https://esp32-auth-api.onrender.com`):

**Opción A: Editar Localmente**

```typescript
// Archivo: frontend/src/app/auth/auth.ts

// CAMBIAR ESTA LÍNEA:
private apiUrl = 'http://localhost:5000/api';

// A ESTO (reemplaza con tu URL):
private apiUrl = 'https://esp32-auth-api.onrender.com/api';
```

Luego:
```bash
cd frontend
git add auth.ts
git commit -m "Actualizar URL del backend para Render"
git push origin main
```

**Opción B: Directamente en Vercel**

Puedes configurarlo como variable de entorno en Vercel (más adelante).

---

### 3️⃣ TERCERO: Desplegar Frontend en Vercel (10 min)

Ahora que el backend está listo:

1. Ve a https://vercel.com
2. Haz click **"New Project"**
3. Selecciona **"Import Git Repository"**
4. Busca `angular_views`
5. Click **"Import"**
6. **Configuración:**
   - **Framework:** Angular
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist/app-esp/browser`
   - **Root Directory:** `frontend` (Vercel lo detecta automáticamente)

7. Click **"Deploy"**
8. Espera 3-5 minutos
9. Tu URL será: `https://angular-views-xxxxx.vercel.app`

**Verifica que funciona:**
```
1. Abre https://angular-views-xxxxx.vercel.app
2. Login con: admin / admin123
3. Deberías ver el dashboard
```

---

## 📝 Configuración Final (Opcional pero Recomendado)

### Agregar CORS Correcto en Backend

Si quieres restringir CORS solo a tu Vercel URL (más seguro):

En `backend/app.py`, línea 20, cambia:
```python
# DE:
CORS(app, resources={r"/api/*": {"origins": "*"}}, ...)

# A:
CORS(app, resources={r"/api/*": {
    "origins": [
        "https://angular-views-xxxxx.vercel.app",
        "http://localhost:4200"
    ]
}}, ...)
```

Luego sube los cambios:
```bash
git add backend/app.py
git commit -m "Restrictar CORS a Vercel y localhost"
git push origin main
```

Render automáticamente hará redeploy.

---

## ✅ CHECKLIST FINAL

```
RENDER (Backend):
[ ] Crear Web Service en Render
[ ] Conectar repositorio angular_views
[ ] Configurar Build Command (cd backend && pip install -r requirements.txt)
[ ] Configurar Start Command (cd backend && gunicorn app:app)
[ ] Agregar variables de entorno (SECRET_KEY, FLASK_ENV)
[ ] Esperar a que esté "Live"
[ ] Copiar URL (ej: https://esp32-auth-api.onrender.com)
[ ] Verificar /api/health

FRONTEND:
[ ] Actualizar auth.ts con URL de Render
[ ] Push a GitHub
[ ] Vercel automáticamente detecta cambios
[ ] Esperar a que redeploy termine

VERIFICACIÓN:
[ ] Abrir Vercel URL
[ ] Login con admin/admin123
[ ] Ver dashboard con datos (si ESP32 envía)
[ ] Verificar que los calls a la API de telemetría funcionen
```

---

## 🔗 URLs FINALES

Después de todo desplegado:

```
📌 Frontend (Vercel):
   https://angular-views-xxxxx.vercel.app

📌 Backend Login (Render):
   https://esp32-auth-api.onrender.com/api/login
   
📌 Health Check (Render):
   https://esp32-auth-api.onrender.com/api/health

📌 API Telemetría (Render anterior):
   https://esp32-server-9ip3.onrender.com/api/telemetry
   (Este NO cambió, es el que trae los datos del ESP32)
```

---

## 🎯 Test de Integración

Una vez todo desplegado, prueba el flujo completo:

```bash
# 1. Test del backend de autenticación
curl -X POST https://esp32-auth-api.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Debe retornar:
# {
#   "success": true,
#   "token": "eyJ0eXAi...",
#   "user": {"id": 1, "username": "admin"}
# }

# 2. Abre el frontend en navegador
# https://angular-views-xxxxx.vercel.app

# 3. Login con admin/admin123

# 4. Deberías ver el dashboard con datos del sensor
```

---

## 🚨 Si Algo Falla

### "Login no funciona en Vercel"
```
1. Verifica que la URL en auth.ts es correcta
2. Abre DevTools (F12) → Network → POST /api/login
3. Busca el error en la respuesta
4. Si es CORS, revisa backend/app.py línea 20
```

### "Backend dice Error 404 en Render"
```
1. Verifica que Procfile existe en backend/
2. Revisa Build Logs en Render
3. Asegúrate que requirements.txt tiene las dependencias
```

### "La tabla de telemetría está vacía"
```
1. Esto es NORMAL si ESP32 no está enviando datos a Render
2. Verifica que ESP32 está configurado para enviar a:
   https://esp32-server-9ip3.onrender.com/api/telemetry
3. Si está enviando, espera 5 segundos (auto-refresh)
```

### "Credenciales inválidas en login"
```
1. Usuario: admin
2. Contraseña: admin123
3. Estos vienen del init_db.py automáticamente
4. Si falla, en Render: Settings → Logs y revisa
```

---

## 📚 Documentación Adicional

En tu repo encontrarás:

- `backend/RENDER_DEPLOYMENT.md` - Detalles técnicos de Render
- `QUICK_START.md` - Resumen rápido
- `DEPLOYMENT_GUIDE.md` - Stack completo
- `README.md` - Índice de todos los documentos

---

## ⏱️ TIEMPO ESTIMADO

| Paso | Tiempo |
|------|--------|
| 1. Deploy Backend en Render | 10 min |
| 2. Actualizar Frontend (auth.ts) | 2 min |
| 3. Deploy Frontend en Vercel | 5 min |
| 4. Verificación | 5 min |
| **TOTAL** | **~22 minutos** |

---

## 🎉 Cuando Todo Esté Listo

Tu app estará en:
```
https://angular-views-xxxxx.vercel.app

Login:
- usuario: admin
- contraseña: admin123

Y podrás ver:
- Datos en tiempo real del ESP32
- Tabla de telemetría con intervalos
- Auto-refresh cada 5 segundos
```

---

**Siguiente paso: Desplegar en Render siguiendo los pasos arriba** 🚀
