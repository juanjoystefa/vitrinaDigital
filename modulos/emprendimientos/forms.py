from django import forms
from .models import Emprendimiento, Productos
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EmprendimientoForm(forms.ModelForm):
    class Meta:
        model = Emprendimiento
        # 1. Agregamos los nuevos campos a la lista
        fields = ["nombre", "descripcion", "link_whatsapp", "link_instagram", "logo"]
        
        # 2. Personalizamos las etiquetas (Lo que lee el usuario)
        labels = {
            'nombre': 'Nombre del Emprendimiento',
            'descripcion': 'Descripción del proyecto',
            'link_whatsapp': 'Número de WhatsApp',
            'link_instagram': 'Enlace de Instagram',
            'logo': 'Logotipo o Imagen'
        }
        
        # 3. Asignamos clases de Bootstrap y textos de ejemplo (placeholders)
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: EcoPlásticos UAO'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Cuéntanos brevemente de qué trata tu emprendimiento...'
            }),
            'link_whatsapp': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: 573001234567 (Código de país + número)'
            }),
            'link_instagram': forms.URLInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: https://instagram.com/tu_cuenta'
            }),
            'logo': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            })
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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Productos
        fields = ["nombre", "descripcion", "precio", "imagen"]
        labels = {
            'nombre': 'Nombre del Producto',
            'descripcion': 'Descripción breve',
            'precio': 'Precio ($)',
            'imagen': 'Foto del producto'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Camiseta Estampada'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Detalles del producto...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 50000', 'step': '0.01'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }