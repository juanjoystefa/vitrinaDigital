from django import forms
from .models import Emprendimiento
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del emprendimiento"})
        }

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añadir las clases de Bootstrap a los campos por defecto del UserCreationForm
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})