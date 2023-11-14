from django import forms
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal, BitacoraGrupalTutor, AnunciosGrupalesTutor


class TutorRegistroForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['numeroEmpleado', 'email', 'password', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'cubiculo', 'telefono']
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': "Escribe la constraseña", 'type': "password"}),
            'numeroEmpleado': forms.TextInput(attrs={'class': 'black-label'}),
            'email': forms.TextInput(attrs={'class': 'black-label'}),
            'nombre': forms.TextInput(attrs={'class': 'black-label'}),
            'apellidoPaterno': forms.TextInput(attrs={'class': 'black-label'}),
            'apellidoMaterno': forms.TextInput(attrs={'class': 'black-label'}),
            'cubiculo': forms.TextInput(attrs={'class': 'black-label'}),
            'telefono': forms.TextInput(attrs={'class': 'black-label'}),
        }


# Crea un nuevo formulario para el inicio de sesión sin estar basado en el modelo Tutor poder realizar el inicio de sesión correctamente sin que se genere el error de unicidad al verificar las credenciales.
class TutorInicioSesionForm(forms.Form):
    numeroEmpleado = forms.CharField(
        max_length=7,
        label='Número de Empleado',
        widget=forms.TextInput(attrs={'class': 'form-control dark-mode-input'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control dark-mode-input',
                   'placeholder': "Escribe la contraseña"}
        ),
        label='Contraseña'
    )


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


class BitacoraGrupalTutorForm(forms.ModelForm):
    class Meta:
        model = BitacoraGrupalTutor
        fields = ['nota']


class AnunciosGrupalesTutorForm(forms.ModelForm):
    class Meta:
        model = AnunciosGrupalesTutor
        fields = ['nota']
