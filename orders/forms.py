from django import forms
from .models import Orden


class OrdenCreateForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['nombre', 'apellidos', 'email', 'direccion', 'codigo_postal', 'ciudad']