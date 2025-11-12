from django import forms
from .models import AsistenteConfig

class AsistenteConfigForm(forms.ModelForm):
    class Meta:
        model = AsistenteConfig
        fields = ['nombre', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input'}),
        }