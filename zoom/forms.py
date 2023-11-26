from django import forms
from crud.models import VideoconferenciasIndividuales, VideoconferenciasGrupales
from django.forms import DateTimeInput


# Creo un formulario para que se puedan crear Reuniones

# class CrearReunionZoomForm(forms.Form):
#     topic = forms.CharField(max_length=80)
#     start_time = forms.DateTimeField(
#         widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

class VideoconferenciasIndividualesForm(forms.ModelForm):
    class Meta:
        model = VideoconferenciasIndividuales
        fields = ['topic', 'start_time']
        labels = {
            'topic': 'Nombre de la reunión *',
            'start_time': 'Hora y fecha *'
        }
        widgets = {
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'start_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }


class VideoconferenciasGrupalesForm(forms.ModelForm):
    class Meta:
        model = VideoconferenciasGrupales
        fields = ['topic', 'start_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ModificarReunionZoomForm(forms.Form):
    topic = forms.CharField(max_length=80)
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    # Agrega otros campos necesarios
