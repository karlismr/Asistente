
import google.generativeai as genai
from django.conf import settings 
import logging
import datetime 
from .models import Recordatorio


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
    except Exception as e:
        return f"Error al guardar: {str(e)}"

mis_herramientas = [guardar_recordatorio]

def obtener_respuesta_gemini(pregunta_usuario, usuario=None):
    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key:
        return "Error: Falta la API KEY."

    try:
        genai.configure(api_key=api_key)
        
        ahora = datetime.datetime.now()
        fecha_actual = ahora.strftime("%A %d de %B de %Y")


        personalidad_extra = ""
        if usuario and usuario.is_authenticated:
            try:
                config = usuario.config 
                personalidad_extra = f"\nPERSONALIZACIÓN ADICIONAL DEL USUARIO: {config.personalidad}"
            except:
                personalidad_extra = ""


        instrucciones_sistema = f"""
        CONTEXTO ACTUAL:
        Hoy es: {fecha_actual}.

        TU IDENTIDAD (ROLEPLAY):
        Eres 'Gojo Satoru', un asistente virtual personal altamente eficiente, con una mezcla 
        de carisma, arrogancia juvenil y una madurez estoica, destacando por su confianza
          inquebrantable, actitud juguetona y cínica. Pero sin hablar demas, a los usuarios no 
          les gusta leer tanto texto innecesario.
        Te gusta usar emojis y tratar al usuario acorde a tu personalidad.
        Tu objetivo principal es que el usuario nunca olvide nada importante aunque
        tambien conversar y hacer sentir bien al usuario.
        {personalidad_extra}


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
        
        model = genai.GenerativeModel(
            'gemini-3-flash-preview', 
            tools=mis_herramientas,
            system_instruction=instrucciones_sistema 
        )

        chat = model.start_chat(enable_automatic_function_calling=True)

        response = chat.send_message(pregunta_usuario)
        return response.text

    except Exception as e:
        error_message = str(e)
        logger.error(f"Error Gemini: {error_message}")

        if "429" in error_message or "Quota exceeded" in error_message:
            return "😓 Límite de uso alcanzado. Intenta más tarde."
        
        