# AGENTS.md - Guía para Asistentes de IA (AI Coding Agents)

Este archivo contiene las directrices, la arquitectura, los comandos clave y las mejores prácticas para cualquier agente de IA que trabaje en este repositorio.

---

## 📌 Descripción del Proyecto

**Asistente Virtual** es una aplicación web desarrollada en **Django 5.2.7** y **Python 3.11** que funciona como un asistente interactivo inteligente. 

### Características principales:
1. **Chat con IA en Tiempo Real**: Integrado con la API de Google Gemini (`gemini-3.1-flash-lite`) utilizando el nuevo SDK oficial `google-genai`. Soporta WebSockets mediante **Django Channels** / Daphne.
2. **Personalización del Asistente**: Cada usuario puede configurar el nombre, la imagen y la personalidad del asistente (por defecto "Satoru Gojo").
3. **Gestión Automática de Recordatorios (Function Calling)**: La IA detecta intenciones de agenda en el texto del usuario y utiliza llamadas a funciones (`registrar_aviso`) para crear objetos `Recordatorio` en la base de datos.
4. **Notificaciones por Telegram**: Comando de gestión de Django (`revisar_recordatorios`) que consulta recordatorios pendientes y los envía a través de un bot de Telegram.
5. **Tareas en Segundo Plano y Cron**: Integración con **Django Q** y webhook secreto (`/ejecutar-cron-secreto/`) para la ejecución programada de revisión de recordatorios.

---

## 📁 Estructura del Repositorio

```text
Asistente/
├── README.md                      # Instrucciones rápidas de uso y despliegue
├── AGENTS.md                      # (Este archivo) Guía para agentes de IA
└── asistentevirtual/              # Directorio principal del proyecto Django
    ├── manage.py                  # CLI de Django
    ├── Dockerfile                 # Configuración de contenedor Docker
    ├── build.sh                   # Script de compilación/despliegue para producción (Render)
    ├── requirements.txt           # Dependencias de Python
    ├── db_usuarios_v1.sqlite3     # Base de datos SQLite local
    ├── mysite/                    # Configuración del proyecto Django
    │   ├── settings.py            # Variables y configuración general
    │   ├── urls.py                # Enrutamiento global de URLs
    │   ├── wsgi.py                # Entrada WSGI (Gunicorn)
    │   └── asgi.py                # Entrada ASGI (Daphne/Channels)
    ├── chat/                      # Aplicación principal Django
    │   ├── models.py              # Modelos: Message, AsistenteConfig, Recordatorio
    │   ├── views.py               # Vistas HTTP: chat, login, registro, cron
    │   ├── consumers.py           # Consumidores WebSocket para Channels
    │   ├── gemini_utils.py        # Integración con el SDK google-genai
    │   ├── tasks.py               # Tareas de verificación en segundo plano
    │   ├── management/commands/   # Comando `revisar_recordatorios.py` (Telegram)
    │   └── templates/chat/        # Plantillas HTML (chat, login, registro, config)
    └── tw_theme/                  # Aplicación de tema Tailwind CSS (django-tailwind)
```

---

## 🛠️ Entorno de Desarrollo y Comandos Clave

> **IMPORTANTE**: Todos los comandos de Django y Python se deben ejecutar desde el directorio `asistentevirtual/`.

```powershell
cd asistentevirtual
```

### 1. Entorno Virtual
- **Activar (Windows PowerShell)**: `.\venv\Scripts\activate`
- **Desactivar**: `deactivate`

### 2. Servidor de Desarrollo
- **Ejecutar servidor HTTP**:
  ```bash
  python manage.py runserver
  ```

### 3. Base de Datos y Migraciones
- **Crear migraciones**: `python manage.py makemigrations`
- **Aplicar migraciones**: `python manage.py migrate`
- Base de datos local: SQLite (`db_usuarios_v1.sqlite3`).
- Base de datos producción: PostgreSQL mediante variable `DATABASE_URL` (vía `dj_database_url`).

### 4. Estilos (Tailwind CSS)
- **Compilar / Modo Watch**:
  ```bash
  python manage.py tailwind start
  ```

### 5. Recopilación de Archivos Estáticos
- **Collectstatic**:
  ```bash
  python manage.py collectstatic --no-input
  ```

### 6. Ejecución del Comando de Recordatorios (Telegram)
- **Revisar y enviar recordatorios pendientes**:
  ```bash
  python manage.py revisar_recordatorios
  ```

### 7. Motor de Tareas en Segundo Plano (Django Q)
- **Iniciar worker**:
  ```bash
  python manage.py qcluster
  ```

### 8. Despliegue con Docker
- **Construir imagen**: `docker build -t asistente .`
- **Correr contenedor**: `docker run -p 10000:10000 --env-file .env asistente`

---

## 🔑 Variables de Entorno (`.env`)

El archivo `.env` se debe ubicar dentro de `asistentevirtual/.env`. Las variables clave requeridas son:

| Variable | Descripción |
| :--- | :--- |
| `GEMINI_API_KEY` | Clave API para autenticación con Google Gemini LLM. |
| `TELEGRAM_BOT_TOKEN` | Token de Bot de Telegram para enviar notificaciones. |
| `TELEGRAM_CHAT_ID` | Chat ID de Telegram hacia donde se envían las alertas. |
| `CLAVE_SECRETA` | Token de seguridad para invocar el endpoint cron `/ejecutar-cron-secreto/?key=<CLAVE_SECRETA>`. |
| `DATABASE_URL` | *(Opcional)* URL de conexión PostgreSQL para producción (Render). |

---

## 🤖 Reglas y Convenciones para Agentes de IA

1. **Análisis Riguroso y Prevención de Rompimientos (CRÍTICO)**: Antes de realizar cualquier modificación, analiza minuciosamente el impacto en los archivos existentes, sus dependencias e integraciones. NUNCA apliques cambios a ciegas; verifica siempre cómo afecta a los demás componentes del proyecto para garantizar una integración fluida y sin regresiones.
2. **Ubicación de Comandos**: Al ejecutar comandos de terminal o herramientas CLI, asegúrate de estar dentro de la carpeta `asistentevirtual/`.
3. **Librería Google Gemini**: Utilizar el nuevo SDK `google-genai` (`from google import genai` y `from google.genai import types`). No reintroducir versiones obsoletas (`google-generativeai`).
4. **Manejo de Respuestas e Intercepción de Funciones**: Preservar el patrón de Function Calling definido en [gemini_utils.py](file:///c:/Users/karli/OneDrive/Documentos/PROGRAMACION/Asistente/asistentevirtual/chat/gemini_utils.py) para que la IA siga extrayendo automáticamente actividades y fechas de recordatorio.
5. **Seguridad y Secretos**: Nunca hardcodear claves o tokens en código fuente. Utilizar siempre `os.environ` o `environ.Env()`.
6. **Asincronía y WebSockets**: En `consumers.py`, utilizar `@sync_to_async` cuando se realicen operaciones síncronas del ORM de Django o llamadas externas síncronas.
7. **Migraciones**: Si modificas modelos en [models.py](file:///c:/Users/karli/OneDrive/Documentos/PROGRAMACION/Asistente/asistentevirtual/chat/models.py), genera la migración con `python manage.py makemigrations` y pruébala localmente antes de dar la tarea por concluida.
