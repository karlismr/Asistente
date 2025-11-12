from django.shortcuts import render, redirect
from .forms import AsistenteConfigForm
from .models import AsistenteConfig, Message


def chat_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(content=content)

    messages = Message.objects.all()

    # Obtener la configuración del asistente (si no existe, usar valores por defecto)
    config = AsistenteConfig.objects.first()
    if not config:
        config = AsistenteConfig(nombre="Asistente Virtual", imagen=None)

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'config': config
    })


def configurar_asistente(request):
    config = AsistenteConfig.objects.first()
    if not config:
        config = AsistenteConfig.objects.create(nombre="Asistente", imagen=None)

    if request.method == 'POST':
        form = AsistenteConfigForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            return redirect('configurar_asistente')  # Redirige después de guardar
    else:
        form = AsistenteConfigForm(instance=config)

    return render(request, 'chat/configurar_asistente.html', {'form': form})