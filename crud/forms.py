from django import forms
from .models import Tutor
from django.contrib.auth.forms import AuthenticationForm


class TutorRegistroForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['numeroEmpleado', 'email', 'password', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'cubiculo', 'telefono']
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': "Escribe la constraseña", 'type': "password"})
        }


# Crea un nuevo formulario para el inicio de sesión sin estar basado en el modelo Tutor poder realizar el inicio de sesión correctamente sin que se genere el error de unicidad al verificar las credenciales.
class TutorInicioSesionForm(forms.Form):
    numeroEmpleado = forms.CharField(max_length=7)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Escribe la contraseña"}))
