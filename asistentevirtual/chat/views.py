import markdown
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import AsistenteConfigForm
from .models import AsistenteConfig, Message
from .gemini_utils import obtener_respuesta_gemini
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def chat_view(request):

    config = AsistenteConfig.objects.first()
    if not config:
        config = AsistenteConfig(nombre="Satoru Gojo", imagen=None)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Guardar el mensaje del USUARIO
            Message.objects.create(content=content, is_user=True)

            # OBTENER RESPUESTA DE GEMINI
            respuesta_ia = obtener_respuesta_gemini(content)
            
            # GUARDAR LA RESPUESTA DE LA IA
            msg_ia = Message.objects.create(content=respuesta_ia, is_user=False)
            respuesta_html = markdown.markdown(respuesta_ia)
            
            return JsonResponse({
                'success': True,
                'ai_response': respuesta_html,
                'timestamp': msg_ia.created_at.strftime("%H:%M")
            })
        
        return JsonResponse({'success': False, 'error': 'No content'})

    messages = Message.objects.all().order_by('created_at')

    # Obtener la configuración del asistente
    
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'config': config
    })

@login_required
def configurar_asistente(request):
    config, created = AsistenteConfig.objects.get_or_create(user=request.user)
    if not config:
        config = AsistenteConfig.objects.create(nombre="Asistente", imagen=None)

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
            login(request, user) # Inicia sesión automáticamente al registrarse
            return redirect('chat_view') 
    else:
        form = UserCreationForm()
    return render(request, 'chat/registro.html', {'form': form})