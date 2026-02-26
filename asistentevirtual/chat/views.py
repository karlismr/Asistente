import markdown
import json
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AsistenteConfigForm
from .models import AsistenteConfig, Message, Recordatorio
from .gemini_utils import obtener_respuesta_gemini
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .management.commands.revisar_recordatorios import Command as RevisarCommand
from django.conf import settings

@login_required
def chat_view(request):
    # Configuración del asistente
    config, created = AsistenteConfig.objects.get_or_create(
        user=request.user, 
        defaults={
            'nombre': 'Satoru Gojo', 
            'personalidad': 'Eres Satoru Gojo de jujustsu kaisen, un personaje carismatico, divertido y poderoso. Responde a las preguntas de manera ingeniosa y con humor, siempre mostrando confianza en ti mismo.'
        }
    )
    personalidad = config.personalidad

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Guardar el mensaje del USUARIO
            Message.objects.create(content=content, is_user=True, user=request.user)

            # Lógica de Recordatorios (Detectar palabras clave)
            palabras_clave = ["recordar", "anota", "agenda", "recuerda", "recuérdame"]
            if any(p in content.lower() for p in palabras_clave):
                try:
                    Recordatorio.objects.create(
                        user=request.user,
                        titulo=content[:200],
                        fecha=timezone.now(), 
                        notificado=False
                    )
                except Exception as e:
                    print(f"Error al guardar recordatorio: {e}")

            # OBTENER RESPUESTA DE GEMINI
            respuesta_ia = obtener_respuesta_gemini(content, personalidad)
            if not respuesta_ia:
                respuesta_ia = "¡Entendido! Ya he anotado eso en tus recordatorios. 😎"
            
            # GUARDAR LA RESPUESTA DE LA IA
            msg_ia = Message.objects.create(content=respuesta_ia, is_user=False, user=request.user)
            respuesta_html = markdown.markdown(respuesta_ia)
            
            return JsonResponse({
                'success': True,
                'ai_response': respuesta_html,
                'timestamp': msg_ia.created_at.strftime("%H:%M")
            })
        
        return JsonResponse({'success': False, 'error': 'No content'})

    # Cargar historial de mensajes para el GET
    messages = Message.objects.filter(user=request.user).order_by('created_at')
    
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'config': config
    })


@login_required
def configurar_asistente(request):
    config, created = AsistenteConfig.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = AsistenteConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            return redirect('chat_view') 
    else:
        form = AsistenteConfigForm(instance=config)
    return render(request, 'chat/configurar_asistente.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_view') 
    else:
        form = UserCreationForm()
    return render(request, 'chat/registro.html', {'form': form})

def ejecutar_revision_cron(request):
    token_recibido = request.GET.get('key')
    if token_recibido == settings.CLAVE_SECRETA:
        try:
            comando = RevisarCommand()
            comando.handle() 
            return JsonResponse({"estado": "exito", "mensaje": "Recordatorios revisados."})
        except Exception as e:
            return JsonResponse({"estado": "error", "mensaje": str(e)}, status=500)
    return JsonResponse({"estado": "error", "mensaje": "No autorizado"}, status=403)