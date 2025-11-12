from django.urls import path
from .views import chat_view, configurar_asistente

urlpatterns = [
    path('', chat_view, name='chat_view'),
      path('configurar/', configurar_asistente, name='configurar_asistente'),
]