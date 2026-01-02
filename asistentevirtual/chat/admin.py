from django.contrib import admin
from .models import AsistenteConfig, Recordatorio


# Permite ver la configuración del asistente
@admin.register(AsistenteConfig)
class AsistenteConfigAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

# Registramos nueva tabla
@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'creado_en') 
    search_fields = ('titulo',) 
    list_filter = ('creado_en',) 