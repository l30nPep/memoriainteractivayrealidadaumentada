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

siguientes 5 documentos de referencia:

- Documento_A: {DOCUMENTOS['Documento_A']}
- Documento_B: {DOCUMENTOS['Documento_B']}
- Documento_C: {DOCUMENTOS['Documento_C']}
- Documento_D: {DOCUMENTOS['Documento_D']}
- Documento_E: {DOCUMENTOS['Documento_E']}
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
