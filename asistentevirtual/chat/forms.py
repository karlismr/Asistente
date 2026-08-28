from django import forms
from .models import AsistenteConfig

class AsistenteConfigForm(forms.ModelForm):
    class Meta:
        model = AsistenteConfig
        fields = ['nombre', 'personalidad', 'imagen', 'imagen_fondo', 'color_encabezado']
        widgets = {
            'personalidad': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ej: Eres un asistente experto en cocina...'}),
            'color_encabezado': forms.TextInput(attrs={'type': 'color', 'class': 'h-10 w-20 p-1 border rounded cursor-pointer'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nombre'].widget.attrs.update({
            'class': 'form-input border rounded'
        })
    
        file_classes = 'block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100'
        
        self.fields['imagen'].widget.attrs.update({
            'class': file_classes
        })

        self.fields['imagen_fondo'].widget.attrs.update({
            'class': file_classes
        })

