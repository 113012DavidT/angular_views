# 🚀 Pasos para Desplegar en Vercel

## Opción 1: Despliegue Automático (Recomendado)

### Paso 1: Conectar GitHub a Vercel
1. Ve a https://vercel.com y haz login (o crea cuenta con GitHub)
2. Haz clic en **"New Project"**
3. Selecciona **"Import Git Repository"**
4. Busca y selecciona `angular_views`
5. Haz clic en **"Import"**

### Paso 2: Configurar Build Settings
1. **Framework Preset**: Selecciona `Angular`
2. **Build Command**: 
   ```
   npm run build
   ```
3. **Output Directory**: 
   ```
   dist/app-esp/browser
   ```
4. **Install Command**: 
   ```
   npm install
   ```

### Paso 3: Environment Variables
1. En la sección "Environment Variables", agrega:
   - **Key**: `API_TELEMETRY_URL`
   - **Value**: `https://esp32-server-9ip3.onrender.com`

2. Haz clic en **"Add"**

### Paso 4: Deploy
1. Haz clic en **"Deploy"**
2. Espera a que termine (2-3 minutos)
3. Vercel te dará una URL como:
   ```
   https://angular-views-xxxxx.vercel.app
   ```

---

## Opción 2: Despliegue Manual (CLI)

### Paso 1: Instalar Vercel CLI
```bash
npm install -g vercel
```

### Paso 2: Login en Vercel
```bash
vercel login
```

### Paso 3: Deploy desde la carpeta frontend
```bash
cd frontend
vercel
```

### Paso 4: Responder preguntas
```
? Set up and deploy "~/frontend"? [Y/n]
? Which scope do you want to deploy to? (tu usuario)
? Link to existing project? [y/N]
? What's your project's name? angular-views
? In which directory is your code located? ./
? Want to modify these settings? [y/N]
? Production Deployment? [Y/n]
```

---

## ✅ Verificación Post-Deploy

### 1. Comprobar que la app está online
```bash
# Abre en navegador:
https://tu-dominio.vercel.app
```

### 2. Verificar que la tabla de telemetría carga
- Login con: `admin` / `admin123`
- En el dashboard, debes ver:
  - 3 tarjetas de datos (Temperatura, Humedad, Estado)
  - Tabla con historial de lecturas del ESP32

### 3. Comprobar conexión a Render API
- Abre DevTools (F12 → Network)
- Recarga la página
- Busca request a `esp32-server-9ip3.onrender.com`
- Debe tener status 200

---

## 🔧 Configuración Avanzada

### Agregar Dominio Personalizado
1. En tu proyecto de Vercel, ve a **Settings** → **Domains**
2. Agrega tu dominio (ej: `miapp.com`)
3. Sigue las instrucciones de DNS

### Variables de Entorno Adicionales (si necesitas)
En **Settings** → **Environment Variables**, puedes agregar:

```
API_AUTH_URL = http://localhost:5000/api
API_TELEMETRY_URL = https://esp32-server-9ip3.onrender.com/api
```

### Edge Functions (Opcional)
Para proteger tu API Render del acceso directo:

Crear `api/_middleware.ts`:
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Aquí puedes agregar lógica de autenticación
  return NextResponse.next();
}
```

---

## 🚨 Troubleshooting

### ❌ Error: "Build failed"
**Solución:**
```bash
# Limpia node_modules y reinstala
rm -rf frontend/node_modules frontend/package-lock.json
cd frontend
npm install
npm run build
```

### ❌ "404 Not Found" en rutas
**Solución:** Vercel.json ya está configurado con rewrites para SPA. Si persiste:
1. En **Settings** → **Build & Development**
2. Verifica que Output Directory sea: `dist/app-esp/browser`

### ❌ "Datos no cargan en el dashboard"
**Solución:**
1. Verifica CORS en Render API
2. En DevTools, busca errores de red
3. Comprueba que la URL de Render es correcta

### ❌ "Service Worker no se registra"
**Solución:**
- PWA requiere HTTPS (Vercel lo proporciona automáticamente)
- Borra caché del navegador
- En DevTools → Application → Service Workers, busca registrado

---

## 📊 Monitoreo en Producción

### Vercel Analytics
1. Ve a tu proyecto en Vercel
2. **Analytics** muestra:
   - Performance (Core Web Vitals)
   - Request frequency
   - Bandwidth usage

### Logs
1. En tu proyecto → **Deployments**
2. Selecciona el último deployment
3. Haz clic en **Logs** para ver errores

---

## 🔄 Actualizar después de cambios

### Actualización Automática
```bash
# En tu repositorio local:
git add .
git commit -m "Actualizar dashboard"
git push origin main
```
✅ Vercel detecta el push y redeploy automáticamente

### Ver historial de deployments
1. Ve a tu proyecto en Vercel
2. **Deployments** muestra todos los cambios
3. Puedes hacer rollback si algo falla

---

## 📦 Build Optimization

Vercel automaticamente:
- Minifica código
- Comprime assets
- Cachea en CDN global
- Sirve desde el servidor más cercano geográficamente

Tamaño final esperado:
```
main-XXXXXX.js   ~85 KB (gzipped)
chunk-XXXXXX.js  ~45 KB (gzipped)
styles-XXXX.css  ~5 KB (gzipped)
```

---

## 🎯 Checklist Final

- [ ] Repositorio pusheado a GitHub
- [ ] Vercel conectado a tu repo
- [ ] Build settings configurados
- [ ] Environment variables agregadas
- [ ] Deploy completado exitosamente
- [ ] App abre sin errores
- [ ] Login funciona (admin/admin123)
- [ ] Dashboard muestra datos del sensor
- [ ] Tabla de telemetría carga
- [ ] Service Worker registrado (PWA)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los **Logs** en Vercel
2. Verifica **Network** en DevTools
3. Crea un issue en GitHub: https://github.com/113012DavidT/angular_views/issues

**¡Tu app estará lista en producción en menos de 5 minutos!** 🎉
