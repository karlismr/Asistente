from django.shortcuts import render, redirect

from .models import Message

def chat_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(content=content)
        return redirect('chat_view')
    
    messages = Message.objects.all().order_by('timestamp')
    return render(request, 'chat/chat.html', {'messages': messages})