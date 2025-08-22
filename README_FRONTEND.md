# LangGraph Marketing Agent - Full Stack Application

Este proyecto ahora incluye un frontend React moderno que se conecta con el agente de marketing LangGraph a través de una API FastAPI.

## 🏗️ Arquitectura del Sistema

### Backend (FastAPI + LangGraph)
- **API REST**: Endpoints para crear y gestionar tareas de marketing
- **WebSocket**: Comunicación en tiempo real para mostrar progreso
- **Agente LangGraph**: Motor de IA con bucle de crítica y refinamiento
- **Integración**: Conecta con el agente original de `main.py`

### Frontend (React + TypeScript)
- **Interfaz moderna**: Diseño responsivo con Tailwind-style CSS
- **Tiempo real**: Conexión WebSocket para ver el progreso en vivo
- **Experiencia de usuario**: Formularios interactivos y visualización de resultados
- **Monitoreo**: Logs en tiempo real como en la terminal

## 🚀 Instrucciones de Uso

### 1. Configuración del Entorno

Asegúrate de tener tu archivo `.env` configurado:
```bash
OPENAI_API_KEY=tu_clave_openai_aqui
```

### 2. Iniciar el Backend

```bash
# Terminal 1: Backend API
cd backend
python main.py
```

La API estará disponible en:
- **API Base**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **WebSocket**: ws://localhost:8000/ws/{client_id}

### 3. Iniciar el Frontend

```bash
# Terminal 2: Frontend React (nueva ventana/pestaña de terminal)
cd frontend
npm start
```

El frontend estará disponible en:
- **Aplicación Web**: http://localhost:3000

### 4. Usar la Aplicación

1. **Abrir el navegador** en http://localhost:3000
2. **Conectar automáticamente** al backend (estado de conexión en la esquina)
3. **Ingresar solicitud** de marketing o seleccionar un ejemplo
4. **Configurar iteraciones** (1-5, recomendado: 3)
5. **Hacer clic en "Generate Marketing Post"**
6. **Ver el progreso en tiempo real** como si fuera la terminal
7. **Revisar los resultados** con investigación y post final

## 🌟 Características Principales

### Frontend React
- ✅ **Interfaz moderna**: Diseño profesional con gradientes y animaciones
- ✅ **Tiempo real**: WebSocket para mostrar progreso como en terminal
- ✅ **Ejemplos predefinidos**: Botones para solicitudes comunes
- ✅ **Configuración flexible**: Control de iteraciones máximas
- ✅ **Monitoreo completo**: Logs detallados con timestamps
- ✅ **Resultados completos**: Post final + investigación + métricas
- ✅ **Responsive**: Funciona en desktop y móvil

### Backend FastAPI
- ✅ **API REST**: Endpoints estándar para integración
- ✅ **WebSocket**: Comunicación bidireccional en tiempo real
- ✅ **CORS**: Configurado para React (localhost:3000)
- ✅ **Documentación**: Swagger UI automática
- ✅ **Gestión de tareas**: Sistema de IDs únicos para seguimiento
- ✅ **Manejo de errores**: Robust error handling y logging

### Integración LangGraph
- ✅ **Agente completo**: Usa el agente original de `main.py`
- ✅ **Estados en tiempo real**: Transmite cada paso del proceso
- ✅ **Bucle crítica-refinamiento**: Funcionalidad completa mantenida
- ✅ **Investigación**: Mock data mejorada transmitida al frontend
- ✅ **Reportes**: Generación automática de informes markdown

## 🔧 Estructura del Proyecto

```
Project Langgraph/
├── main.py                     # Agente LangGraph original (línea de comandos)
├── requirements.txt            # Dependencias Python originales
├── backend/
│   ├── main.py                # FastAPI server + WebSocket
│   └── requirements.txt       # Dependencias backend adicionales
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Aplicación React principal
│   │   ├── App.css            # Estilos CSS modernos
│   │   └── components/
│   │       └── MarketingAgent.tsx  # Componente principal
│   ├── package.json           # Dependencias Node.js
│   └── public/                # Archivos estáticos
└── README.md                  # Esta documentación
```

## 🎯 Flujo de Trabajo

### 1. Usuario Inicia Generación
- Usuario ingresa solicitud en el frontend
- Frontend crea tarea vía POST /api/marketing/generate
- WebSocket se conecta para actualizaciones en tiempo real

### 2. Backend Procesa
- **Investigación**: Análisis de mercado y audiencia
- **Redacción inicial**: Generación del primer borrador
- **Crítica**: Evaluación automática del contenido
- **Refinamiento**: Mejoras iterativas basadas en críticas
- **Finalización**: Generación de reporte completo

### 3. Frontend Muestra Progreso
- **Barra de progreso**: 0-100% visual
- **Logs en tiempo real**: Como output de terminal
- **Estados detallados**: Cada paso del proceso
- **Resultados finales**: Post + investigación + métricas

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI**: Framework web Python moderno
- **Uvicorn**: Servidor ASGI de alta performance
- **WebSockets**: Comunicación en tiempo real
- **LangGraph**: Motor de agentes IA existente
- **OpenAI GPT-4**: Modelo de lenguaje para generación

### Frontend
- **React 18**: Library de UI moderna
- **TypeScript**: Tipado estático para JavaScript
- **Axios**: Cliente HTTP para APIs
- **Lucide React**: Iconos modernos
- **CSS3**: Estilos modernos con animaciones

## 🔍 Debugging y Desarrollo

### Logs del Backend
Los logs del servidor FastAPI mostrarán:
- Conexiones WebSocket
- Creación de tareas
- Progreso de generación
- Errores del sistema

### DevTools del Frontend
En Chrome DevTools podrás ver:
- Mensajes WebSocket en Network tab
- Logs de React en Console
- Estados de la aplicación

### Pruebas de Conexión
1. **Backend health check**: http://localhost:8000/health
2. **API docs**: http://localhost:8000/docs
3. **Frontend**: http://localhost:3000

## 🚧 Próximas Mejoras

- [ ] **Aprobación humana**: Integrar flujo de aprobación interactivo
- [ ] **Historial**: Guardar y mostrar generaciones anteriores
- [ ] **Plantillas**: Sistema de plantillas personalizables
- [ ] **Analytics**: Métricas de performance del agente
- [ ] **Exportar**: Múltiples formatos de exportación
- [ ] **Configuración avanzada**: Parámetros de modelo ajustables

## 🤝 Contribución

1. El agente original mantiene toda su funcionalidad
2. El backend FastAPI es una capa adicional no intrusiva
3. El frontend puede usarse independientemente
4. Ambos sistemas pueden ejecutarse por separado

---

**¡Disfruta tu nuevo Marketing Agent con interfaz web moderna!** 🚀

El sistema original de línea de comandos sigue funcionando exactamente igual, y ahora tienes la opción adicional de una interfaz web completa con monitoreo en tiempo real.
