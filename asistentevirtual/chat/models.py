from django.db import models


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_user = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{'User' if self.is_user else 'AI'}: {self.content[:30]}..."


class AsistenteConfig(models.Model):
    nombre = models.CharField(max_length=100, default="Mi Asistente")
    imagen = models.ImageField(upload_to='asistente/', null=True, blank=True)

    def __str__(self):
        return self.nombre