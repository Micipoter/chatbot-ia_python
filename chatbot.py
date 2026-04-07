from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
from config import PROMPT_SISTEMA

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Falta API_KEY en el archivo .env")

# Cliente OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# Inicializar FastAPI
app = FastAPI()

# Modelo de entrada
class Pregunta(BaseModel):
    pregunta: str
    user_id: str = "default"  # identificador de usuario

# Memoria en RAM (contexto)
historial_por_usuario = {}

# Modelos con fallback
MODELOS = [
    "meta-llama/llama-3-8b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "nvidia/nemotron-3-super-120b-a12b:free"
]

@app.post("/chat")
def obtener_respuesta(p: Pregunta):
    try:
        user_id = p.user_id

        # Inicializar historial si no existe
        if user_id not in historial_por_usuario:
            historial_por_usuario[user_id] = []

        historial = historial_por_usuario[user_id]

        ultimo_error = None

        for modelo in MODELOS:
            try:
                print(f"🔄 Usuario {user_id} | Modelo: {modelo}")

                # Construir mensajes con contexto
                mensajes_base = [
                    {
                        "role": "system",
                        "content": PROMPT_SISTEMA + "\n\nResponde siempre en español de forma clara y no muy extensa."
                    },
                    *historial,
                    {
                        "role": "user",
                        "content": p.pregunta
                    }
                ]

                # Primera llamada (reasoning)
                response = client.chat.completions.create(
                    model=modelo,
                    messages=mensajes_base,
                    extra_body={"reasoning": {"enabled": True}}
                )

                if not response.choices:
                    continue

                message = response.choices[0].message

                # Segunda llamada (refinamiento)
                mensajes_refinados = [
                    *mensajes_base,
                    {
                        "role": "assistant",
                        "content": message.content,
                        "reasoning_details": getattr(message, "reasoning_details", None)
                    },
                    {
                        "role": "user",
                        "content": "Verifica tu respuesta, corrígela si es necesario y responde en español de forma breve."
                    }
                ]

                response2 = client.chat.completions.create(
                    model=modelo,
                    messages=mensajes_refinados,
                    extra_body={"reasoning": {"enabled": True}}
                )

                if not response2.choices:
                    continue

                respuesta = response2.choices[0].message.content.strip()

                if not respuesta:
                    continue

                # Limitar tamaño de respuesta
                respuesta = respuesta[:1500]

                # Guardar en historial
                historial.append({"role": "user", "content": p.pregunta})
                historial.append({"role": "assistant", "content": respuesta})

                # Limitar historial (últimos 10 mensajes)
                historial_por_usuario[user_id] = historial[-10:]

                return {
                    "modelo_usado": modelo,
                    "respuesta": respuesta,
                    "mensajes_en_contexto": len(historial_por_usuario[user_id])
                }

            except Exception as e:
                print(f"❌ Error con {modelo}: {e}")
                ultimo_error = str(e)
                continue

        raise Exception(f"Todos los modelos fallaron. Último error: {ultimo_error}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))