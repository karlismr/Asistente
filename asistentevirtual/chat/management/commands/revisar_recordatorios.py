import asyncio
from django.core.management.base import BaseCommand
from django.utils import timezone
from chat.models import Recordatorio
from telegram import Bot

class Command(BaseCommand):
    help = 'Revisa recordatorios pendientes y los envia por telegram'

    def handle(self, *args, **options):
        TOKEN = '8078848240:AAF52zntA0U4yKuD6NLAWENub2w366mXaXU'
        CHAT_ID = '806030060'

        bot = Bot(token=TOKEN)
        ahora = timezone.now()

        pendientes = Recordatorio.objects.filter(
            fecha__lte=ahora, 
            notificado=False
        )

        if not pendientes.exists():
            self.stdout.write(self.style.SUCCESS('No hay recordatorios pendientes por ahora.'))
            return

        for r in pendientes:
           mensaje = f"🔔 ¡RECORDATORIO! 🔔\n\nHola {r.user.username}, paso por aqui porque no se te puede olvidar esto😉: \n📌 {r.titulo}"
           try:
            
                asyncio.run(bot.send_message(chat_id=CHAT_ID, text=mensaje, parse_mode='Markdown'))

                r.notificado = True
                r.save()  

                self.stdout.write(self.style.SUCCESS(f'Recordatorio enviado a {r.user.username}: {r.titulo}'))

              
           except Exception as e:
               
                self.stdout.write(self.style.ERROR(f'Error al enviar recordatorio a {r.user.username}: {e}'))
                
           
        