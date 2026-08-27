from django.core.management.base import BaseCommand
from chat.models import Message

class Command(BaseCommand):
    help = 'Corrige automáticamente los valores del campo is_user en el historial de mensajes'

    def handle(self, *args, **options):
        ai_prefixes = ('¡', 'lo siento', 'vaya,', 'gojo está', 'genial:', 'error:', '😓', 'hola! ¿cómo va todo?', 'hola! ¿qué tal?', 'hola! ¡aquí')
        ai_keywords = ('técnica infinita', 'hechicero más fuerte', 'revisa los logs', 'infinito (spoiler', 'mi técnica', 'agendado tu recordatorio', 'recordatorio guardado', 'estoy muy feliz de verte')

        actualizados = 0
        for m in Message.objects.all():
            c_lower = (m.content or "").strip().lower()
            es_ai = any(c_lower.startswith(p) for p in ai_prefixes) or any(k in c_lower for k in ai_keywords)
            deberia_ser_user = not es_ai
            if m.is_user != deberia_ser_user:
                m.is_user = deberia_ser_user
                m.save()
                actualizados += 1

        self.stdout.write(self.style.SUCCESS(f'Corrección completada con éxito. Registros corregidos: {actualizados}'))
