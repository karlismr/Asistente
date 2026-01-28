from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_user = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anónimo'} - {'User' if self.is_user else 'AI'}: {self.content[:30]}..."

class AsistenteConfig(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="config")
    nombre = models.CharField(max_length=100, default="Mi Asistente")
    personalidad = models.TextField(default="Eres un asistente amable y servicial.") 
    imagen = models.ImageField(upload_to='asistente/', null=True, blank=True)

    def __str__(self):
        return f"Config de {self.user.username}"

class Recordatorio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminders")
    titulo = models.CharField(max_length=200)
    fecha = models.DateTimeField() 
    creado_en = models.DateTimeField(auto_now_add=True)
    notificado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.titulo} - {self.fecha}"