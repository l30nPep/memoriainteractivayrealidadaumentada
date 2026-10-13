import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
app = FastAPI()
# Permitir que tu frontend de GitHub Pages se conecte al backend
app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # En producción, cambia esto por tu URL de
GitHub Pages
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)
# Inicializar cliente de Gemini (busca automáticamente la variable
GEMINI_API_KEY
client = genai.Client()

# Tu base de conocimientos estática
DOCUMENTOS = {
"Documento_A": "Información sobre horarios, precios de
entradas, ubicación del museo y políticas de reembolso.",
"Documento_B": "Guía de solución de problemas técnicos,
reinicio de contraseñas y cómo contactar a soporte.",
"Documento_C": "Catálogo de productos disponibles, stock de
remeras, talles y envíos a todo el país.",
"Documento_D": "Historia de la empresa, misión, visión y
biografías de los fundadores.",
"Documento_E": "Términos y condiciones legales, políticas de
privacidad y uso de cookies."
}
class ConsultaRequest(BaseModel):
pregunta: str
@app.post("/preguntar")
async def procesar_pregunta(request: ConsultaRequest):
try:
# Construimos un System Instruction dinámico que obliga a

la IA a actuar como Router

instrucciones_sistema = f"""
Eres un asistente inteligente. Tienes acceso a los

siguientes 6 documentos de referencia:

- Cerro_Chenque: {DOCUMENTOS['Cerro_Chenque']}
- Faro_san_Jorge: {DOCUMENTOS['Faro_san_Jorge']}
- Museo_Regional_Patagonico: {DOCUMENTOS['Documento_C']}
- Museo_Ferroportuario: {DOCUMENTOS['Museo_Ferroportuario']}
- Barrio_Mosconi: {DOCUMENTOS['Barrio_mosconi']}
- Barrio_Astra: {DOCUMENTOS['Barrio_Astra']}
Tu tarea:
1. Analiza la pregunta del usuario.
2. Deduce cuál de los 5 documentos contiene la información

necesaria para responder.

3. Responde a la pregunta del usuario utilizando

exclusivamente la información de ese documento.

4. Sé breve, directo y conciso, ya que tu respuesta será

leída en voz alta.
"""
# Llamada a la API de Gemini (usando el modelo rápido

flash)

response = client.models.generate_content(
model='gemini-2.5-flash',
contents=request.pregunta,
config=types.GenerateContentConfig(

system_instruction=instrucciones_sistema,
temperature=0.3 # Baja temperatura para evitar que

invente cosas (alucine)

)
)
return {"respuesta": response.text}
except Exception as e:
raise HTTPException(status_code=500, detail=str(e))
