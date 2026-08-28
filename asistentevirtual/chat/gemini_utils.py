import traceback
from django.conf import settings 
import logging
import datetime 
from .models import Recordatorio
from google import genai 
from google.genai import types

logger = logging.getLogger(__name__)

# --- 1. FUNCIÓN PARA GUARDAR EN LA BASE DE DATOS ---
from django.utils.dateparse import parse_datetime
from django.utils import timezone

def guardar_recordatorio(actividad: str, fecha_recordatorio: str, user):
    """
    Guarda un recordatorio en la base de datos.
    """
    try:
        dt = None
        if fecha_recordatorio:
            str_fecha = str(fecha_recordatorio).strip()
            dt = parse_datetime(str_fecha)
            if not dt:
                for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
                    try:
                        dt = datetime.datetime.strptime(str_fecha, fmt)
                        break
                    except ValueError:
                        continue
        
        if dt and timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        fecha_final = dt if dt else fecha_recordatorio

        recordatorio = Recordatorio.objects.create(
            user=user,
            titulo=actividad,
            fecha=fecha_final
        )
        logger.info(f"--- RECORDATORIO AGENDADO EXITOSAMENTE: '{user}' agendó '{actividad}' para '{fecha_final}' ---")
        return f"Genial: Recordatorio guardado para {fecha_final}."
    except Exception:
        error_db = traceback.format_exc()
        logger.error(f"Error al escribir recordatorio en BD: {error_db}")
        return "Error técnico al guardar en base de datos."


# --- 2. LA HERRAMIENTA PARA LA IA ---
def registrar_aviso(actividad: str, fecha_recordatorio: str):
    """
    Guarda un recordatorio en la base de datos.
    Args:
        actividad: La tarea o evento a recordar (ej: 'Ir a la peluquería').
        fecha_recordatorio: Fecha y hora exacta en formato 'YYYY-MM-DD HH:MM:SS' (ej: '2026-08-28 10:00:00').
    """
    return {"actividad": actividad, "fecha_recordatorio": fecha_recordatorio}


def es_intencion_recordatorio(texto: str) -> bool:
    palabras_clave = [
        "record", "recuerda", "recuerdame", "recuérdame", "agendar", "agenda",
        "tengo que", "cita", "evento", "avisar", "avísame", "avisame",
        "guardar recordatorio", "anotar", "anota", "programar", "mañana tengo",
        "tengo un", "tengo una", "peluqueria", "peluquería", "dentista", "medico", "médico"
    ]
    texto_lower = str(texto).lower()
    return any(kw in texto_lower for kw in palabras_clave)


# --- 3. FUNCIÓN PRINCIPAL DE GEMINI ---
def obtener_respuesta_gemini(pregunta_usuario, personalidad, user):
    api_key = getattr(settings, "GEMINI_API_KEY", None)

    if not api_key:
        return "Error: No se encontro la API KEY en settings.py."

    try:
        client = genai.Client(api_key=api_key)
        
        ahora = datetime.datetime.now()
        fecha_actual = ahora.strftime("%A %d de %B de %Y")
        hora_actual = ahora.strftime("%H:%M")

        instrucciones_sistema = f"""
        CONTEXTO ACTUAL:
        Hoy es: {fecha_actual}.
        Hora actual: {hora_actual}.

        TU IDENTIDAD:
        {personalidad}

        REGLAS OBLIGATORIAS DE GESTIÓN DE RECORDATORIOS (CRÍTICO):
        Tienes acceso a la herramienta `registrar_aviso`.
        
        1. SIEMPRE QUE EL USUARIO SOLICITE UN RECORDATORIO, CITA, EVENTO O TAREA (ej: "recuérdame...", "tengo que ir...", "guarda un recordatorio..."), ES ABSOLUTAMENTE OBLIGATORIO E IMPRESCINDIBLE QUE EJECUTES LA FUNCIÓN `registrar_aviso`.
        2. NUNCA respondas simulando con solo texto que agendaste o guardaste el recordatorio si NO has invocado la función `registrar_aviso`.
        3. El parámetro `fecha_recordatorio` DEBE estar en formato 'YYYY-MM-DD HH:MM:SS'. Calcula la fecha exacta basándote en que hoy es {fecha_actual} y la hora actual es {hora_actual}.

        CASO A: EL USUARIO NO ESPECIFICA CUÁNDO RECORDAR
        Si el usuario dice "Tengo un evento tal fecha" pero NO dice cuándo quiere que le avises, 
        debes ser proactivo y llamar a la función `registrar_aviso` MÚLTIPLES VECES para cubrir estos plazos:
        1. 1 mes antes del evento.
        2. 1 semana antes del evento.
        3. El día anterior al evento.
        4. El mismo día del evento 6 horas antes.
        
        CASO B: EL USUARIO ESPECIFICA CUÁNDO RECORDAR
        Si el usuario dice explícitamente cuándo quiere el aviso (ej: "Recuérdame mañana a las 10am" o "Avísame 3 días antes"),
        obedece strictly la solicitud del usuario, llamando a la función para las fechas pedidas.
        """

        mode_fc = types.FunctionCallingConfigMode.ANY if es_intencion_recordatorio(pregunta_usuario) else types.FunctionCallingConfigMode.AUTO

        config = types.GenerateContentConfig(
            system_instruction=instrucciones_sistema,
            tools=[registrar_aviso],
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode=mode_fc
                )
            ),
            temperature=0.3
        )


        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=pregunta_usuario,
            config=config
        )

        # --- INTERCEPTOR DE LLAMADAS DE FUNCIÓN ---
        if response.function_calls:
            agendados = []
            for call in response.function_calls:
                if call.name == 'registrar_aviso':
                    args = call.args
                    act = args.get('actividad')
                    fec = args.get('fecha_recordatorio')
                    guardar_recordatorio(
                        actividad=act,
                        fecha_recordatorio=fec,
                        user=user
                    )
                    agendados.append(f"'{act}' para {fec}")
            
            if agendados:
                return f"¡Entendido! He registrado en la base de datos tu recordatorio: {', '.join(agendados)}."

        return response.text if response.text else ''

    except Exception:
        error_completo = traceback.format_exc()
        logger.error(f"Fallo en el flujo de Gemini: {error_completo}")

        if "429" in error_completo:
            return "😓 Límite de cuota alcanzado (muchas preguntas). Intenta en un minuto."

        return "Lo siento, hubo un error técnico. Revisa los logs de la consola."



# --- 4. WRAPPER FINAL (MANTENIDO IDÉNTICA) ---
def guardar_con_usuario(actividad: str, fecha_recordatorio: str, user):
    """Wrapper que pasa user a guardar_recordatorio"""
    return guardar_recordatorio(actividad, fecha_recordatorio, user=user)