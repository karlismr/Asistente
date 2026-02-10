from django.contrib import admin
from .models import AsistenteConfig, Recordatorio


@admin.register(AsistenteConfig)
class AsistenteConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'personalidad') 
    
    # Esto organiza como se ven los datos cuando haces clic para editar
    fields = ('user', 'nombre_asistente', 'personalidad', 'imagen')
    

# Registramos nueva tabla
@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'creado_en') 
    search_fields = ('titulo',) 
    list_filter = ('creado_en',) 
