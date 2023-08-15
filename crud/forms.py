from django import forms
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal


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


class TutoradoRegistroForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = ['boletaTutorado', 'email', 'password', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'semestre', 'telefono']
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': "Escribe la constraseña", 'type': "password"})
        }

# Crea un nuevo formulario para el inicio de sesión sin estar basado en el modelo Tutorado poder realizar el inicio de sesión correctamente sin que se genere el error de unicidad al verificar las credenciales.


class TutoradoInicioSesionForm(forms.Form):
    boletaTutorado = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': "Escribe la contraseña"}))


class TutoriaIndividualForm(forms.ModelForm):
    class Meta:
        model = TutoriaIndividual
        fields = ['idTutorado', 'nombreTutoriaIndividual']


class BitacoraIndividualTutorForm(forms.ModelForm):
    class Meta:
        model = BitacoraIndividualTutor
        fields = ['nota']


class NotasIndividualesTutoradoForm(forms.ModelForm):
    class Meta:
        model = NotasIndividualesTutorado
        fields = ['nota']


class TutoriaGrupalForm(forms.ModelForm):
    class Meta:
        model = TutoriaGrupal
        fields = ['nombreGrupo', 'salon']
