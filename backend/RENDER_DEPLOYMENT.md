# 🚀 Desplegar Backend en Render

## Instrucciones Paso a Paso

### Paso 1: Preparar el Repositorio

```bash
# El backend debe estar en backend/ del repositorio
# Archivos necesarios:
✅ app.py
✅ init_db.py
✅ requirements.txt
✅ Procfile
✅ runtime.txt
✅ .env.example
```

### Paso 2: Crear Nuevo Servicio en Render

1. Ve a https://render.com
2. Haz clic en **"New +"** → **"Web Service"**
3. Selecciona **"Connect a repository"**
4. Busca y conecta tu repo `angular_views`

### Paso 3: Configurar el Servicio

**Name:** (ej: `esp32-auth-api` o `angular-views-auth`)

**Environment:** 
- Selecciona **"Python 3"**

**Build Command:**
```bash
cd backend && pip install -r requirements.txt
```

**Start Command:**
```bash
cd backend && gunicorn app:app
```

### Paso 4: Variables de Entorno

En **"Environment"**, agrega:

```
SECRET_KEY = tu-clave-secreta-aqui (genera una aleatoria)
FLASK_ENV = production
PORT = 5000
```

**Ejemplo de SECRET_KEY:**
```
SECRET_KEY = a7f3c9e1b2d4f6h8j0k2l4m6n8p0q2r4s6t8u0v2w4x6y8z0a2b4c6d8e0f2g4
```

### Paso 5: Deploy

1. Haz clic en **"Create Web Service"**
2. Render detectará `Procfile` y compilará automáticamente
3. Espera 3-5 minutos hasta que esté "Live"
4. Tu URL será: `https://tu-servicio.onrender.com`

### Paso 6: Verificar

```bash
# Test del health check
curl https://tu-servicio.onrender.com/api/health

# Respuesta esperada:
# {"status": "ok", "message": "API funcionando correctamente"}
```

### Paso 7: Obtener URL para el Frontend

Tu URL final será algo como:
```
https://esp32-auth-api.onrender.com
```

O lo que haya aparecido en la página de Render.

---

## Actualizar Frontend con la URL

Una vez tengas la URL del backend en Render, actualiza en `frontend/src/app/auth/auth.ts`:

```typescript
// ANTES:
private apiUrl = 'http://localhost:5000/api';

// DESPUÉS:
private apiUrl = 'https://tu-servicio.onrender.com/api';
```

---

## Troubleshooting

### "Build failed"
```
1. Verifica que requirements.txt esté correcto
2. Asegúrate que Procfile exista
3. Revisa Build Logs en Render
```

### "Port already in use"
```
Render automáticamente detecta PORT del entorno
No cambies el puerto en app.py
```

### "Login no funciona después del deploy"
```
1. Verifica SECRET_KEY en Render environment
2. Comprueba CORS en app.py (está habilitado para todos)
3. Revisa los logs: Settings → Logs
```

### "Database no se inicializa"
```
Render automáticamente corre: python init_db.py (release command)
Si falla, revisa Logs en Render
```

---

## Monitoreo

### Ver logs en producción
1. En Render, tu servicio → **"Logs"**
2. Busca errores HTTP o de BD
3. Si hay 500 errors, revisa la excepción en los logs

### Health Check
```bash
# Verifica que la API está activa
curl https://tu-servicio.onrender.com/api/health
```

---

## URLs Finales

Una vez desplegado:

| Servicio | URL |
|----------|-----|
| **Backend Auth** | `https://tu-servicio.onrender.com` |
| **Health Check** | `https://tu-servicio.onrender.com/api/health` |
| **Login Endpoint** | `https://tu-servicio.onrender.com/api/login` |

---

## Importante

⚠️ **Cambios a hacer:**

1. En `app.py`:
   - Verificar que CORS está permitido para tu Vercel URL
   - En producción, cambiar `SECRET_KEY`

2. En `frontend/src/app/auth/auth.ts`:
   - Reemplazar `localhost:5000` con tu URL de Render

3. En Render:
   - Configurar SECRET_KEY fuerte
   - Monitorear logs regularmente

---

**Tiempo estimado de despliegue: 5-10 minutos**
