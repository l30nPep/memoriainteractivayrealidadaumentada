import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types

app = FastAPI()
# Inicializamos la aplicación
app = Flask(_name_)

# Configuramos el cliente de Gemini (asegúrate de tener tu API Key configurada en tu sistema)
client = genai.Client()

@app.route("/", methods=["GET", "POST"])
def puente_ia():
    pregunta_usuario = ""
    respuesta_ia = ""
    
    # Cuando el usuario le da a "Enviar" en la página
    if request.method == "POST":
        # 1. Python recibe la pregunta que mandó el HTML
        pregunta_usuario = request.form.get("pregunta", "")
        
        if pregunta_usuario:
            try:
                # 2. Python le manda la pregunta a Gemini y espera la respuesta
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=pregunta_usuario,
                )
                # 3. Guardamos la respuesta que dio la IA
                respuesta_ia = response.text
            except Exception as e:
                respuesta_ia = f"Ocurrió un error al conectar con Gemini: {e}"
                
    # 4. Devolvemos todo a la página web para que se muestre en pantalla
    return render_template("index.html", pregunta=pregunta_usuario, respuesta=respuesta_ia)

# Permitir que tu frontend de GitHub Pages se conecte al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, puedes cambiarlo por la URL de tu GitHub Pages
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar cliente de Gemini (busca automáticamente la variable GEMINI_API_KEY)
client = genai.Client()

# Tu base de conocimientos estática
DOCUMENTOS = {
    "Cerro_Chenque": "informacion sobre el Cerro Chenque, ubicacion y por que es un lugar historico el Cerro Chenque.",
    "Faro_san_Jorge": "informacion sobre el Faro san Jorge, ubicacion y por que es un lugar historico el Faro san Jorge.",
    "Museo_Regional_Patagonico": "informacion sobre el Museo Regional Patagonico, ubicacion y por que es un lugar historico el Museo Regional Patagonico.",
    "Museo_Ferroportuario": "informacion sobre el Museo Ferroportuario, ubicacion y por que es un lugar historico el Museo Ferroportuario.",
    "Barrio_Mosconi": "informacion sobre el Barrio Mosconi, ubicacion y por que es un lugar historico el Barrio Mosconi",
    "Barrio_Astra": "informacion sobre el Barrio Astra, ubicacion y por que es un lugar historico el Barrio Astra."
}

class ConsultaRequest(BaseModel):
    pregunta: str

@app.post("/preguntar")
async def procesar_pregunta(request: ConsultaRequest): 
    try:
        instrucciones_sistema = f"""
Eres un asistente inteligente. Tienes acceso a los siguientes 6 documentos de referencia:

- Cerro_Chenque: {DOCUMENTOS['Cerro_Chenque']}
- Faro_san_Jorge: {DOCUMENTOS['Faro_san_Jorge']}
- Museo_Regional_Patagonico: {DOCUMENTOS['Museo_Regional_Patagonico']}
- Museo_Ferroportuario: {DOCUMENTOS['Museo_Ferroportuario']}
- Barrio_Mosconi: {DOCUMENTOS['Barrio_Mosconi']}
- Barrio_Astra: {DOCUMENTOS['Barrio_Astra']}

Tu tarea:
1. Analiza la pregunta del usuario.
2. Deduce cuál de los 6 documentos contiene la información necesaria para responder.
3. Responde a la pregunta del usuario utilizando exclusivamente la información de ese documento.
4. Sé breve, directo y conciso, ya que tu respuesta será leída en voz alta.
"""
        # Llamada a la API de Gemini
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=request.pregunta,
            config=types.GenerateContentConfig(
                system_instruction=instrucciones_sistema,
                temperature=0.3
            )
        )
        return {"respuesta": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
