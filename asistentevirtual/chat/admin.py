from django.contrib import admin
from .models import AsistenteConfig, Recordatorio


@admin.register(AsistenteConfig)
class AsistenteConfigAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombre', 'personalidad', 'color_encabezado') 
    fields = ('user', 'nombre', 'personalidad', 'imagen', 'imagen_fondo', 'color_encabezado')

    

# Registramos nueva tabla
@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'creado_en') 
    search_fields = ('titulo',) 
    list_filter = ('creado_en',) 
