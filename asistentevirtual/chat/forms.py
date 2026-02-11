from django import forms
from .models import AsistenteConfig

class AsistenteConfigForm(forms.ModelForm):
    class Meta:
        model = AsistenteConfig
        fields = ['nombre', 'personalidad', 'imagen']
        widgets = {
            'personalidad': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ej: Eres un asistente experto en cocina...'}),
        }
        
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            self.fields['nombre'].widget.attrs.update({
                'class': 'form-input border rounded'
            })
        
            self.fields['imagen'].widget.attrs.update({
                'class': 'block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100'
            })
