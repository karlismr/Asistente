from django.utils import timezone
from datetime import timedelta
from chat.models import Recordatorio 

def verificar_eventos_proximos():
    """
    Busca eventos que ocurrirán en la próxima hora y no han sido notificados.
    """
    ahora = timezone.now()
    tiempo_limite = ahora + timedelta(hours=1)
   
    eventos = Recordatorio.objects.filter(
        fecha__gt=ahora,       # Que sea en el futuro
        fecha__lte=tiempo_limite, # Pero antes de 1 hora
        notificado=False              # Y que no hayamos avisado ya
    )

    print(f"Buscando eventos... Encontrados: {eventos.count()}")

    for evento in eventos:
        print(f"Recordando evento: {evento.nombre} a las {evento.fecha_inicio}")
        
        # Aquí va la función de enviar notificación
        
        evento.notificado = True
        evento.save()
    
    return f"Procesados {eventos.count()} eventos"