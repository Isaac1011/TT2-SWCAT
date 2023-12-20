from django import forms
from .models import Tutor, Tutorado, TutoriaIndividual, BitacoraIndividualTutor, NotasIndividualesTutorado, TutoriaGrupal, BitacoraGrupalTutor, AnunciosGrupalesTutor


class TutorRegistroForm(forms.ModelForm):

    class Meta:
        model = Tutor
        fields = [
            'numeroEmpleado', 'email', 'password', 'nombre',
            'apellidoPaterno', 'apellidoMaterno', 'cubiculo', 'telefono', 'acepta_terminos', 'acepta_privacidad'
        ]
        labels = {
            'password': 'Contraseña *',
            'numeroEmpleado': 'Número de Empleado *',
            'email': 'Email *',
            'nombre': 'Nombre *',
            'apellidoPaterno': 'Apellido paterno *',
            'apellidoMaterno': 'Apellido materno *',
            'cubiculo': 'Sala de la Tutora o el Tutor *',
            'telefono': 'Número de teléfono *',
            'acepta_terminos': 'He leído y acepto los Términos y Condiciones *',
            'acepta_privacidad': 'He leído y acepto el Aviso de privacidad *'
        }
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': "Ingrese una contraseña válida para registrarse en el sistema (máximo 25 caracteres)", 'type': "password", 'class': 'form-control dark-mode-input password-input'}),
            'numeroEmpleado': forms.TextInput(attrs={'placeholder': "Número de empleado de la Tutora o el Tutor", 'class': 'form-control dark-mode-input'}),
            'email': forms.TextInput(attrs={'placeholder': "Correo electrónico para ser asociado a la cuenta principal de Zoom", 'class': 'form-control dark-mode-input'}),
            'nombre': forms.TextInput(attrs={'placeholder': "Nombre de la Tutora o el Tutor", 'class': 'form-control dark-mode-input'}),
            'apellidoPaterno': forms.TextInput(attrs={'placeholder': "Apelldio paterno de la Tutora o el Tutor", 'class': 'form-control dark-mode-input'}),
            'apellidoMaterno': forms.TextInput(attrs={'placeholder': "Apellido materno de la Tutora o el Tutor", 'class': 'form-control dark-mode-input'}),
            'cubiculo': forms.TextInput(attrs={'placeholder': "Sala de la Tutora o el Tutor (máximo 100 caracteres)", 'class': 'form-control dark-mode-input'}),
            'telefono': forms.TextInput(attrs={'placeholder': "Número de teléfono de la Tutora o Tutor", 'class': 'form-control dark-mode-input'}),
            'acepta_terminos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acepta_privacidad': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


# Crea un nuevo formulario para el inicio de sesión sin estar basado en el modelo Tutor poder realizar el inicio de sesión correctamente sin que se genere el error de unicidad al verificar las credenciales.
class TutorInicioSesionForm(forms.Form):
    numeroEmpleado = forms.CharField(
        max_length=7,
        label='Número de Empleado *',
        widget=forms.TextInput(attrs={
                               'class': 'form-control dark-mode-input', 'placeholder': 'Ingrese su Número de Empleado'})
    )
    password = forms.CharField(
        label='Contraseña *',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control dark-mode-input',
                   'placeholder': "Ingrese la contraseña asociada a su Número de Empleado"}
        )

    )


class TutoradoRegistroForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = ['boletaTutorado', 'email', 'password', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'genero', 'semestre', 'telefono', 'acepta_terminos', 'acepta_privacidad']
        labels = {
            'password': 'Contraseña *',
            'boletaTutorado': 'Número de Boleta *',
            'email': 'Correo electrónico *',
            'nombre': 'Nombre *',
            'apellidoPaterno': 'Apellido paterno *',
            'apellidoMaterno': 'Apellido materno *',
            'genero': 'Género',
            'semestre': 'Número de semestre que estás cursando *',
            'telefono': 'Número de teléfono *',
            'acepta_terminos': 'He leído y acepto los Términos y Condiciones *',
            'acepta_privacidad': 'He leído y acepto el Aviso de privacidad *'
        }
        widgets = {
            'password': forms.TextInput(attrs={'placeholder': "Ingrese una contraseña válida para registrarse en el sistema (máximo 25 caracteres)", 'type': "password", 'class': 'form-control dark-mode-input password-input'}),
            'boletaTutorado': forms.TextInput(attrs={'placeholder': "Número de boleta del Tutorado", 'class': 'form-control dark-mode-input'}),
            'email': forms.TextInput(attrs={'placeholder': "Correo electrónico del Tutorado", 'class': 'form-control dark-mode-input'}),
            'nombre': forms.TextInput(attrs={'placeholder': "Nombre del Tutorado", 'class': 'form-control dark-mode-input'}),
            'apellidoPaterno': forms.TextInput(attrs={'placeholder': "Apellido paterno del Tutorado", 'class': 'form-control dark-mode-input'}),
            'apellidoMaterno': forms.TextInput(attrs={'placeholder': "Apellido materno del Tutorado", 'class': 'form-control dark-mode-input'}),
            'genero': forms.Select(choices=[('Mujer', 'Mujer'), ('Hombre', 'Hombre'), ('Otro', 'Otro')],
                                   attrs={'class': 'form-control dark-mode-input'}),
            'semestre': forms.Select(choices=[(i, i) for i in range(1, 13)], attrs={'class': 'form-control dark-mode-input'}),
            'telefono': forms.TextInput(attrs={'placeholder': "Número de teléfono del Tutorado", 'class': 'form-control dark-mode-input'}),
            'acepta_terminos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acepta_privacidad': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


# Crea un nuevo formulario para el inicio de sesión sin estar basado en el modelo Tutorado poder realizar el inicio de sesión correctamente sin que se genere el error de unicidad al verificar las credenciales.


class TutoradoInicioSesionForm(forms.Form):
    boletaTutorado = forms.CharField(
        max_length=10,
        label='Número de Boleta *',
        widget=forms.TextInput(attrs={
                               'class': 'form-control dark-mode-input', 'placeholder': 'Ingrese su Número de Boleta'})
    )
    password = forms.CharField(
        label='Contraseña *',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control dark-mode-input',
                   'placeholder': "Ingrese la contraseña asociada a su Número de Boleta"}
        )
    )

# Crea un nuevo formulario para la creción de tutorias individuales sin estar basado en el modelo TutoriaIndividual poder realizar el registro correctamente


class TutoriaIndividualForm(forms.Form):
    boletaTutorado = forms.CharField(
        max_length=10,
        label='Número de Boleta *',
        widget=forms.TextInput(attrs={
                               'class': 'form-control dark-mode-input', 'placeholder': 'Número de Boleta del Tutorado'})
    )

    nombreTutoriaIndividual = forms.CharField(
        max_length=45,
        label='Nombre de Tutoría Individual *',
        widget=forms.TextInput(
            attrs={'class': 'form-control dark-mode-input', 'placeholder': 'Identificar la tutoría fácilmente (números, letras, caracteres especiales con un máximo de 45 caracteres)', })
    )


class BitacoraIndividualTutorForm(forms.ModelForm):

    opciones_choices = [
        ('Acompañamiento', 'Acompañamiento durante la trayectoria escolar'),
        ('Orientacion', 'Orientación sobre servicios y trámites'),
        ('Atencion', 'Atención especializada y canalización'),
        ('Pertenencia', 'Pertenencia Institucional'),
    ]

    intervencion = forms.MultipleChoiceField(
        choices=opciones_choices,
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
    )

    class Meta:
        model = BitacoraIndividualTutor
        fields = ['nota', 'intervencion']
        labels = {
            'intervencion': '¿Qué temas se abordaron el la sesión de tutoría? Puede seleccionar más de una opción: *',

            'nota': 'Bitácora *',
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control dark-mode-input', 'rows': 7, 'placeholder': 'Escriba las acciones que se realizaron durante la sesión de tutoría (máximo 1000 caracteres)'}),
        }


class NotasIndividualesTutoradoForm(forms.ModelForm):
    class Meta:
        model = NotasIndividualesTutorado
        fields = ['nota']
        labels = {
            'nota': 'Nota *',
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control', 'rows': 7, 'placeholder': 'Escriba la nota que desea guardar en el sistema (máximo 1000 caracteres)'}),
        }


class TutoriaGrupalForm(forms.ModelForm):
    class Meta:
        model = TutoriaGrupal
        fields = ['nombreGrupo', 'salon']
        labels = {
            'nombreGrupo': 'Nombre del Grupo *',
            'salon': 'Salón *',
        }
        widgets = {
            'nombreGrupo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Identificar la tutoría fácilmente (números, letras, caracteres especiales con un máximo de 45 caracteres)', }),
            'salon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Salón del grupo o posibles reuniones del grupo', }),
        }


class BitacoraGrupalTutorForm(forms.ModelForm):

    opciones_choices = [
        ('Acompañamiento', 'Acompañamiento durante la trayectoria escolar'),
        ('Orientacion', 'Orientación sobre servicios y trámites'),
        ('Atencion', 'Atención especializada y canalización'),
        ('Pertenencia', 'Pertenencia Institucional'),
    ]

    intervencion = forms.MultipleChoiceField(
        choices=opciones_choices,
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}),
    )

    class Meta:
        model = BitacoraGrupalTutor
        fields = ['nota', 'intervencion']
        labels = {
            'nota': 'Bitácora *'
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control dark-mode-input', 'rows': 7, 'placeholder': 'Escriba las acciones que se realizaron durante la sesión de tutoría (máximo 1000 caracteres)'}),
        }


class AnunciosGrupalesTutorForm(forms.ModelForm):
    class Meta:
        model = AnunciosGrupalesTutor
        fields = ['nota']
        labels = {
            'nota': 'Nota *'
        }
        widgets = {
            'nota': forms.Textarea(attrs={'class': 'form-control dark-mode-input', 'rows': 7, 'placeholder': 'Escriba el anuncio que desea informa a los tutorados inscritos a esta Tutoría Grupal (máximo 1000 caracteres)'}),
        }


class TutorForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['numeroEmpleado', 'zoomUserID', 'email', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'cubiculo', 'telefono']

        widgets = {
            'numeroEmpleado': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'zoomUserID': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidoPaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidoMaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'cubiculo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'numeroEmpleado': 'Número de Empleado',
            'zoomUserID': 'ID Zoom',
            'email': 'Correo Electrónico',
            'nombre': 'Nombre',
            'apellidoPaterno': 'Apellido Paterno',
            'apellidoMaterno': 'Apellido Materno',
            'cubiculo': 'Sala del Tutor',
            'telefono': 'Teléfono',
        }


class TutoradoForm(forms.ModelForm):
    class Meta:
        model = Tutorado
        fields = ['boletaTutorado', 'email', 'nombre',
                  'apellidoPaterno', 'apellidoMaterno', 'genero', 'semestre', 'telefono']

        widgets = {
            'boletaTutorado': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidoPaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellidoMaterno': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(choices=[('Mujer', 'Mujer'), ('Hombre', 'Hombre'), ('Otro', 'Otro')],
                                   attrs={'class': 'form-control'}),
            'semestre': forms.Select(choices=[(i, i) for i in range(1, 13)], attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'boletaTutorado': 'Boleta del Tutorado',
            'email': 'Correo Electrónico',
            'nombre': 'Nombre',
            'apellidoPaterno': 'Apellido Paterno',
            'apellidoMaterno': 'Apellido Materno',
            'genero': 'Género',
            'semestre': 'Número de semestre que estás cursando',
            'telefono': 'Teléfono',
        }
