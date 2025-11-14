
import google.generativeai as genai
from django.conf import settings # Para leer la API Key desde settings.py

# Configurar Gemini con la clave de API
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("Modelo Gemini configurado exitosamente.")
except Exception as e:
    print(f"ERROR: No se pudo configurar Gemini. Revisa tu API_KEY. Error: {e}")
    model = None

def obtener_respuesta_gemini(pregunta_usuario):
    """
    Envía la pregunta a Gemini y devuelve la respuesta.
    """
    if model is None:
        return "Lo siento, el servicio de IA no está configurado correctamente."

    try:
        response = model.generate_content(pregunta_usuario)
        return response.text
    except Exception as e:
        print(f"Error al contactar a Gemini: {e}")
        return "Lo siento, no pude conectarme con la IA en este momento."