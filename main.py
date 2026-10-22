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
#GitHub Pages
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)
# Inicializar cliente de Gemini (busca automáticamente la variable
GEMINI_API_KEY
client = genai.Client()

# Tu base de conocimientos estática
DOCUMENTOS = {
"Barrio_Astra": "Información de que es, por que es un lugar historico y donde se ubica el Barrio Astra.",
"Barrio_mosconi": "Información de que es, por que es un lugar historico y donde se ubica el Barrio Mosconi.",
"Museo_Ferroportuario": "Información de que es, por que es un lugar historico y donde se ubica el Museo Ferroportuario.",
"Cerro_Chenque": "Información de que es, por que es un lugar historico y donde se ubica el Cerro Chenque.",
"Museo_Nacional_del_Petroleo": "Información de que es, por que es un lugar historico y donde se ubica el Museo Nacional del Petroleo.",
"Museo_Regional_patagonico": "Información de que es, por que es un lugar historico y donde se ubica el Museo Regional Patagonico."
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

- Barrio_Astra: {DOCUMENTOS['Barrio_Astra']}
- Barrio_Mosconi: {DOCUMENTOS['Barrio_mosconi']}
- Museo_Ferroportuario: {DOCUMENTOS['Museo_Ferroportuario']}
- Cerro_Chenque: {DOCUMENTOS['Cerro_Chenque']}
- Museo_Nacional_del_Petroleo: {DOCUMENTOS['Museo_Nacional_del_Petroleo']}
- Museo_Regional_patagonico: {DOCUMENTOS['Museo_Regional_Patagonico']}
Tu tarea:
1. Analiza la pregunta del usuario.
2. Deduce cuál de los 5 documentos contiene la información

necesaria para responder.

3. Responde a la pregunta del usuario utilizando

exclusivamente la información de ese documento.

4. Sé breve, directo y conciso, ya que tu respuesta será

leída en voz alta.
"""
# Llamada a la API de Gemini (usando el modelo rápido flash)

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
