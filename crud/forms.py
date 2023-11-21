from django import forms
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal, BitacoraGrupalTutor, AnunciosGrupalesTutor


class TutorRegistroForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['numeroEmpleado', 'email', 'password', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'cubiculo', 'telefono']
        labels = {
            'password': 'Contraseña *',
            'numeroEmpleado': 'Número de Empleado *',
            'email': 'Email *',
            'nombre': 'Nombre *',
            'apellidoPaterno': 'Apellido paterno *',
            'apellidoMaterno': 'Apellido materno *',
            'cubiculo': 'Cubículo',
            'telefono': 'Número de teléfono'
        }
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': "", 'type': "password", 'class': 'form-control dark-mode-input', 'style': 'color: #ec0000'}),
            'numeroEmpleado': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'email': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'apellidoPaterno': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'apellidoMaterno': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'cubiculo': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
        }


# Crea un nuevo formulario para el inicio de sesión sin estar basado en el modelo Tutor poder realizar el inicio de sesión correctamente sin que se genere el error de unicidad al verificar las credenciales.
class TutorInicioSesionForm(forms.Form):
    numeroEmpleado = forms.CharField(
        max_length=7,
        label='Número de Empleado *',
        widget=forms.TextInput(attrs={'class': 'form-control dark-mode-input'})
    )
    password = forms.CharField(
        label='Contraseña *',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control dark-mode-input',
                   'placeholder': ""}
        )

    )


class TutoradoRegistroForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = ['boletaTutorado', 'email', 'password', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'semestre', 'telefono']
        labels = {
            'password': 'Contraseña *',
            'boletaTutorado': 'Número de Boleta *',
            'email': 'Correo electrónico *',
            'nombre': 'Nombre *',
            'apellidoPaterno': 'Apellido paterno *',
            'apellidoMaterno': 'Apellido materno *',
            'semestre': 'Número de semestre',
            'telefono': 'Número de teléfono',
        }
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': "", 'type': "password", 'class': 'form-control dark-mode-input'}),
            'boletaTutorado': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'email': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'apellidoPaterno': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'apellidoMaterno': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'semestre': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control dark-mode-input'}),


        }

# Crea un nuevo formulario para el inicio de sesión sin estar basado en el modelo Tutorado poder realizar el inicio de sesión correctamente sin que se genere el error de unicidad al verificar las credenciales.


class TutoradoInicioSesionForm(forms.Form):
    boletaTutorado = forms.CharField(
        max_length=10,
        label='Número de Boleta *',
        widget=forms.TextInput(attrs={'class': 'form-control dark-mode-input'})
    )
    password = forms.CharField(
        label='Contraseña *',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control dark-mode-input',
                   'placeholder': ""}
        )
    )


class TutoriaIndividualForm(forms.ModelForm):
    class Meta:
        model = TutoriaIndividual
        fields = ['idTutorado', 'nombreTutoriaIndividual']


class BitacoraIndividualTutorForm(forms.ModelForm):
    class Meta:
        model = BitacoraIndividualTutor
        fields = ['nota']
        labels = {
            'nota': 'Bitácora: *'
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control dark-mode-input', 'rows': 7}),
        }


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
        labels = {
            'nota': 'Bitácora: *'
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control dark-mode-input', 'rows': 7}),
        }


class AnunciosGrupalesTutorForm(forms.ModelForm):
    class Meta:
        model = AnunciosGrupalesTutor
        fields = ['nota']
