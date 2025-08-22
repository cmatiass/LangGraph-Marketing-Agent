# 🚀 Guía de Despliegue en Render - LangGraph Marketing Agent

## ✅ Configuración Completa para Render

### 📋 Campos de Configuración en Render

Cuando crees el servicio web en Render, usa estos valores:

| Campo | Valor | Descripción |
|-------|--------|-------------|
| **Root Directory** | *(vacío)* | Usar la raíz del repositorio |
| **Build Command** | `cd frontend && npm ci && npm run build && mkdir -p ../backend/static && cp -r build/* ../backend/static/ && cd ../backend && pip install -r requirements.txt` | Compila frontend y backend |
| **Start Command** | `cd backend && uvicorn main:app --host=0.0.0.0 --port=$PORT` | Inicia el servidor unificado |
| **Environment Variables** | `OPENAI_API_KEY=tu_api_key_aqui` | Tu clave de OpenAI |
| **Pre-Deploy Command** | *(vacío)* | No necesario |

### 🌍 Variables de Entorno Requeridas

```env
OPENAI_API_KEY=tu_clave_de_openai_aqui
```

### 📁 Estructura del Proyecto para Render

```
Project Langgraph/
├── backend/
│   ├── main.py              # Servidor FastAPI + archivos estáticos
│   ├── requirements.txt     # Dependencias Python
│   └── static/             # Frontend compilado (auto-generado)
├── frontend/
│   ├── package.json        # Dependencias React
│   ├── src/               # Código fuente React
│   └── build/             # Build de producción (auto-generado)
├── render-config.md        # Esta guía
└── README.md
```

## 🔧 Características del Despliegue Unificado

### ✅ Lo Que Funciona
- **Una sola URL**: Frontend y backend en el mismo dominio
- **Sin CORS**: No hay problemas de origen cruzado
- **WebSocket**: Funciona sin configuración adicional
- **Routing React**: Todas las rutas del frontend funcionan
- **API REST**: Todos los endpoints `/api/*` disponibles

### 🌐 URLs Disponibles
- **Frontend**: `https://tu-app.onrender.com/`
- **API Health**: `https://tu-app.onrender.com/health`
- **API Docs**: `https://tu-app.onrender.com/docs`
- **WebSocket**: `wss://tu-app.onrender.com/ws/{client_id}`

## 🚀 Pasos para Desplegar

### 1. Subir a GitHub
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

### 2. Crear Servicio en Render
1. Ve a [Render.com](https://render.com)
2. Crea nuevo "Web Service"
3. Conecta tu repositorio de GitHub
4. Usa la configuración de la tabla de arriba

### 3. Configurar Variables de Entorno
- `OPENAI_API_KEY`: Tu clave de OpenAI GPT-4

### 4. Deploy
- Render automáticamente ejecutará el build y deploy
- El proceso toma ~5-10 minutos

## ⚡ Comandos de Build Explicados

```bash
# 1. Compilar frontend React
cd frontend && npm ci && npm run build

# 2. Copiar build al backend
mkdir -p ../backend/static && cp -r build/* ../backend/static/

# 3. Instalar dependencias del backend
cd ../backend && pip install -r requirements.txt
```

## 🔍 Verificación Local

Para probar antes de desplegar:

```bash
# 1. Build el frontend
cd frontend
npm run build

# 2. Copiar al backend
cd ..
mkdir -p backend/static
cp -r frontend/build/* backend/static/

# 3. Ejecutar servidor unificado
cd backend
python main.py
```

Visita: `http://localhost:8000`

## 🎯 Características de Producción

### Frontend
- ✅ Build optimizado de React
- ✅ Detección automática de entorno
- ✅ URLs dinámicas para API
- ✅ WebSocket con protocolo automático

### Backend
- ✅ Sirve archivos estáticos del frontend
- ✅ API REST completa
- ✅ WebSocket para tiempo real
- ✅ Routing catch-all para React

### Funcionalidades Completas
- ✅ Generación de posts con IA
- ✅ Bucle de crítica y refinamiento
- ✅ Panel de aprobación humana
- ✅ Feedback específico del usuario
- ✅ Monitoreo en tiempo real
- ✅ Reportes automáticos en Markdown

## 🎉 Resultado Final

Una vez desplegado en Render, tendrás:

- **URL pública única** para tu aplicación
- **Frontend React** moderno y responsivo
- **Backend API** completo con WebSocket
- **Sistema de feedback humano** completamente funcional
- **Escalabilidad automática** proporcionada por Render

¡Tu LangGraph Marketing Agent estará disponible para todo el mundo! 🌍✨
