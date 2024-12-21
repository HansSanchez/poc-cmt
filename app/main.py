import openai
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Carga las variables del archivo .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("La clave OPENAI_API_KEY no está configurada. Verifica tu archivo .env y la configuración de Docker.")

app = FastAPI()
print("Iniciando FastAPI...")

# Lista única de orígenes permitidos
origins = [
    "*",  # Desarrollo local
]

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Lista única de orígenes
    allow_credentials=False,  # Habilitado para cookies o autenticación
    allow_methods=["POST"],  # Métodos permitidos
    allow_headers=["*"],  # Permitir todos los encabezados
)
print("Configuración de CORS completada.")

# Crea un cliente de OpenAI
client = openai.Client(
    api_key=api_key
)
print("Cliente de OpenAI creado.")

@app.post("/poc-openai/")
def poc_openai(message: str = Form(...)):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {"role": "user", "content": message}
            ],
            max_tokens=150,
            temperature=1
        )
        response_text = response.choices[0].message.content.strip()
        return {"response": response_text}
    except Exception as e:
        print(f"Error al comunicarse con OpenAI: {e}")
        raise HTTPException(status_code=500, detail=f"Error al comunicarse con OpenAI: {e}")
