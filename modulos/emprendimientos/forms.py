from django import forms
from .models import Emprendimiento

class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre del emprendimiento"})
        }