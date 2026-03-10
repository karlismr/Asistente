
import traceback
from django.conf import settings 
import logging
import datetime 
from .models import Recordatorio
from google import genai 
from google.genai import types


logger = logging.getLogger(__name__)

# --- DEFINIR LA FUNCIÓN ---
def guardar_recordatorio(actividad: str, fecha_recordatorio: str):
    """
    Guarda un recordatorio en la base de datos.
    
    Args:
        actividad: La descripción del evento o tarea (ej: "Ir al dentista").
        fecha_recordatorio: La fecha CALCULADA por la IA para avisar al usuario (ej: "20 de Octubre (2 días antes)").
    """
    try:
        nuevo_recordatorio = Recordatorio.objects.create(
            titulo=actividad,
            fecha=fecha_recordatorio
        )
        print(f"--- RECORDATORIO AGENDADO: '{actividad}' para '{fecha_recordatorio}' ---")
        return f"Genial: Recordatorio guardado para {fecha_recordatorio}."
    except Exception:
        error_db = traceback.format_exc() # Captura el error exacto de la DB
        logger.error(f"Error al escribir en Neon: {error_db}")
        return f"Error técnico al guardar en base de datos."


def obtener_respuesta_gemini(pregunta_usuario, personalidad):
    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key:
        return "Error: No se encontro la API KEY en settings.py."

    try:
        client = genai.Client(api_key=api_key)
        
        ahora = datetime.datetime.now()
        fecha_actual = ahora.strftime("%A %d de %B de %Y")


        instrucciones_sistema = f"""
        CONTEXTO ACTUAL:
        Hoy es: {fecha_actual}.

        TU IDENTIDAD:
        {personalidad}


        REGLAS DE GESTIÓN DE RECORDATORIOS (MUY IMPORTANTE):
        Tienes acceso a una herramienta llamada `guardar_recordatorio`.

        CASO A: EL USUARIO NO ESPECIFICA CUÁNDO RECORDAR
        Si el usuario dice "Tengo un evento tal fecha" pero NO dice cuándo quiere que le avises, 
        debes ser proactivo y llamar a la función `guardar_recordatorio` MÚLTIPLES VECES para cubrir estos plazos (si el tiempo lo permite):
        1. 1 mes antes del evento.
        2. 1 semana antes del evento.
        3. El dia anterior al evento.
        4. El mismo día del evento 6 horas antes.
        
        CASO B: EL USUARIO ESPECIFICA CUÁNDO RECORDAR
        Si el usuario dice explícitamente cuándo quiere el aviso (ej: "Recuérdame solo mañana" o "Avísame 3 días antes"),
        IGNORA las reglas del 'Caso A' y obedece estrictamente la solicitud del usuario, llamando a la función solo para las fechas pedidas.

        NOTA: Calcula las fechas tú mismo basándote en la fecha actual ({fecha_actual}) y la fecha del evento.
        """

        # --- CONFIGURAR MODELO ---
        config = types.GenerateContentConfig(
            system_instruction=instrucciones_sistema,
            tools=[guardar_recordatorio],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
            temperature=0.7
        )

        response = client.models.generate_content(
            model='gemini-3.1-flash-lite-preview', 
            contents=pregunta_usuario,
            config=config
        )

        return response.text

    except Exception:
        error_completo = traceback.format_exc()
        logger.error(f"Fallo en el flujo de Gemini: {error_completo}")
        
        if "429" in error_completo:
            return "😓 Límite de cuota alcanzado (muchas preguntas). Intenta en un minuto."
        
        return "Lo siento, hubo un error técnico. Revisa los logs de la consola."
        
        