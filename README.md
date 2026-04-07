# 🤖 Chatbot API experto en Python (con memoria y reasoning)

Este proyecto es una API REST basada en FastAPI que funciona como un chatbot experto en Python 🐍. Utiliza modelos de IA a través de OpenRouter (compatible con la API de OpenAI) e incorpora:

- 🧠 Memoria de conversación por usuario
- 🔁 Fallback automático de modelos
- ⚡ Reasoning avanzado (respuestas más precisas)
- 🗣️ Respuestas en español
- 🛡️ Manejo de errores robusto

---

## 🚀 Requisitos

- Python 3.8 o superior
- API Key de OpenRouter
- Conexión a internet

---

## 🛠 Instalación

1. Clona este repositorio o descarga los archivos.

2. Crea un entorno virtual:

```bash
python -m venv venv
```

3. Activa el entorno virtual:

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Instala dependencias:

```bash
pip install -r requirements.txt
```

5. Crea un archivo `.env` en la raíz:

```env
API_KEY=tu_api_key_de_openrouter
```

---

## ▶️ Ejecución

```bash
uvicorn chatbot:app --reload
```

- API: http://127.0.0.1:8000
- Docs (Swagger): http://127.0.0.1:8000/docs

---

## 📬 Uso de la API

**Endpoint:** `POST /chat`

**Body:**

```json
{
  "pregunta": "¿Qué es una función en Python?",
  "user_id": "usuario1"
}
```

---

## 🧠 Contexto (IMPORTANTE)

El campo `user_id` permite mantener memoria de conversación.

**Ejemplo:**

1️⃣
```json
{
  "pregunta": "¿Qué es una lista en Python?",
  "user_id": "juan"
}
```

2️⃣
```json
{
  "pregunta": "¿Y cómo se recorre?",
  "user_id": "juan"
}
```

👉 El bot recuerda la conversación anterior.

**✅ Respuesta:**

```json
{
  "modelo_usado": "meta-llama/llama-3-8b-instruct:free",
  "respuesta": "Una lista en Python es una colección ordenada...",
  "mensajes_en_contexto": 4
}
```

---

## 🧠 Características principales

### 🔹 Memoria por usuario
- Guarda historial en memoria (RAM)
- Mantiene contexto de conversación
- Límite de últimos 10 mensajes

### 🔹 Fallback de modelos
Si un modelo falla (429 o 404), usa otro automáticamente:
- `meta-llama/llama-3-8b-instruct:free`
- `mistralai/mistral-7b-instruct:free`
- `nvidia/nemotron-3-super-120b-a12b:free`

### 🔹 Reasoning avanzado
- Mejora precisión de respuestas
- Verificación automática de respuestas
- Corrección interna del modelo

### 🔹 Especialización en Python
Definida en `config.py`:
- Explicaciones claras
- Ejemplos de código
- Buenas prácticas
- Restringido al tema Python

### 🔹 Respuestas en español
El sistema fuerza respuestas claras y en español.

---

## ⚠️ Limitaciones actuales

- ❌ Memoria no persistente (se pierde al reiniciar)
- ❌ No hay autenticación de usuarios
- ❌ No hay base de datos
- ❌ Dependencia de modelos gratuitos (pueden fallar)

---

## 🐳 Despliegue con Docker

```bash
docker build -t python-chatbot .
```

```bash
docker run -d -p 8000:8000 --name chatbot --env-file .env python-chatbot
```

---

## ☁️ Despliegue en Render

1. Crear un Web Service
2. Conectar repositorio
3. Configurar variables de entorno
4. Start command:

```bash
uvicorn chatbot:app --host 0.0.0.0 --port 8000
```

---

## 📁 Estructura del proyecto

```
chatbot-ia_python/
├── chatbot.py        # API principal con FastAPI
├── config.py         # PROMPT_SISTEMA (comportamiento del bot)
├── .env              # API KEY
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🚀 Próximas mejoras (roadmap)

- 💾 Persistencia con base de datos (SQLite/PostgreSQL)
- 🔐 Autenticación de usuarios
- 🌐 Frontend tipo ChatGPT
- ⚡ Streaming en tiempo real
- 📊 Logs y monitoreo

---

## 👨‍💻 Autor

**Ing. Cristian Díaz**

<p align="center">
  <img width="300" src="https://i.imgur.com/a7YBcsp.png">
</p>