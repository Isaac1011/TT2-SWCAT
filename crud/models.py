from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
import secrets


# Create your models here.


class Tutor(models.Model):
    idTutor = models.AutoField(primary_key=True)
    numeroEmpleado = models.CharField(max_length=7, unique=True)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    nombre = models.CharField(max_length=45)
    apellidoPaterno = models.CharField(max_length=45)
    apellidoMaterno = models.CharField(max_length=45)
    cubiculo = models.CharField(max_length=100, default=None)
    telefono = models.CharField(max_length=10, default=None)
    zoomUserID = models.CharField(
        max_length=30, default=None, null=True, blank=True)
    acepta_terminos = models.BooleanField(default=False)
    acepta_privacidad = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Antes de guardar, convierte la contraseña en un hash seguro
        if self.password:
            self.password = make_password(self.password)

        # Llama al método save() de la clase padre para manejar el guardado del objeto
        super(Tutor, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.numeroEmpleado} - {self.nombre} {self.apellidoPaterno} {self.apellidoMaterno}'


class Tutorado(models.Model):
    idTutorado = models.AutoField(primary_key=True)
    boletaTutorado = models.CharField(max_length=10, unique=True)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    nombre = models.CharField(max_length=45)
    apellidoPaterno = models.CharField(max_length=45)
    apellidoMaterno = models.CharField(max_length=45)
    genero = models.CharField(max_length=6, default=None)
    semestre = models.CharField(max_length=2, default=None)
    telefono = models.CharField(max_length=10, default=None)
    numTutoresAsignados = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])
    acepta_terminos = models.BooleanField(default=False)
    acepta_privacidad = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Antes de guardar, convierte la contraseña en un hash seguro
        if self.password:
            self.password = make_password(self.password)

        # Llama al método save() de la clase padre para manejar el guardado del objeto
        super(Tutorado, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.boletaTutorado} - {self.nombre} {self.apellidoPaterno} {self.apellidoMaterno}'


class TutoriaIndividual(models.Model):
    idTutoriaIndividual = models.AutoField(primary_key=True)
    idTutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    idTutorado = models.ForeignKey(Tutorado, on_delete=models.CASCADE)
    nombreTutoriaIndividual = models.CharField(max_length=45)

    def __str__(self):
        return f"Tutoría Individual de {self.idTutor} a {self.idTutorado}"


class BitacoraIndividualTutor(models.Model):
    idBitacoraIndividual = models.AutoField(primary_key=True)
    # Relación con el modelo TutoriaIndividual
    idTutoriaIndividual = models.ForeignKey(
        TutoriaIndividual, on_delete=models.CASCADE)
    # Notas o contenido de la bitácora
    nota = models.CharField(max_length=1000)
    # Fecha y hora de la entrada de la bitácora (se establece automáticamente con el parámetro auto_now_add en la creación de la bitácora)
    fecha = models.DateTimeField(auto_now_add=True)
    intervencion = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return f"idBitacoraIndividual: {self.idBitacoraIndividual} - idTutoriaIndividual: {self.idTutoriaIndividual}"


class NotasIndividualesTutorado(models.Model):
    idNotasIndividualesTutorado = models.AutoField(primary_key=True)
    # Relación con el modelo TutoriaIndividual
    idTutoriaIndividual = models.ForeignKey(
        TutoriaIndividual, on_delete=models.CASCADE)
    # Descripción de la nota
    nota = models.CharField(max_length=1000)
    # Fecha y hora de la entrada de la bitácora
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"idNotasIndividualesTutorado: {self.idNotasIndividualesTutorado} - idTutoriaIndividual: {self.idTutoriaIndividual}"


class TutoriaGrupal(models.Model):
    idTutoriaGrupal = models.AutoField(primary_key=True)
    idTutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    nombreGrupo = models.CharField(max_length=45, default=None)
    cupoDisponible = models.IntegerField(default=45)
    salon = models.CharField(max_length=100, default=None)
    passwordGrupo = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"idTutoriaGrupal: {self.idTutoriaGrupal} - idTutor: {self.idTutor} - nombreGrupo: {self.nombreGrupo}"


class ListaTutoriaGrupal(models.Model):
    idListaTutoriaGrupal = models.AutoField(primary_key=True)
    # Relación con el modelo TutoriaGrupal
    idTutoriaGrupal = models.ForeignKey(
        TutoriaGrupal, on_delete=models.CASCADE)
    # Relación con el modelo Tutorado
    idTutorado = models.ForeignKey(Tutorado, on_delete=models.CASCADE)

    def __str__(self):
        return f"idListaTutoriaGrupal: {self.idListaTutoriaGrupal} - idTutoriaGrupal: {self.idTutoriaGrupal} - idTutorado: {self.idTutorado}"


class BitacoraGrupalTutor(models.Model):
    idBitacoraGrupalTutor = models.AutoField(primary_key=True)
    idTutoriaGrupal = models.ForeignKey(
        TutoriaGrupal, on_delete=models.CASCADE)
    nota = models.CharField(max_length=1000)
    # Fecha y hora de la entrada de la bitácora (se establece automáticamente con el parámetro auto_now_add en la creación de la bitácora)
    fecha = models.DateTimeField(auto_now_add=True)
    intervencion = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return f"idBitacoraGrupalTutor: {self.idBitacoraGrupalTutor} - idTutoriaGrupal: {self.idTutoriaGrupal}"


class AnunciosGrupalesTutor(models.Model):
    idAnunciosGrupalesTutor = models.AutoField(primary_key=True)
    idTutoriaGrupal = models.ForeignKey(
        TutoriaGrupal, on_delete=models.CASCADE)
    nota = models.CharField(max_length=1000)
    # Fecha y hora de la entrada de la bitácora (se establece automáticamente con el parámetro auto_now_add en la creación de la bitácora)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"idAnunciosGrupalesTutor: {self.idAnunciosGrupalesTutor} - idTutoriaGrupal: {self.idTutoriaGrupal}"


class VideoconferenciasIndividuales(models.Model):
    idVideoconferenciaIndivual = models.AutoField(primary_key=True)
    idTutoriaIndividual = models.ForeignKey(
        TutoriaIndividual, on_delete=models.CASCADE)
    topic = models.CharField(max_length=80)
    start_time = models.DateTimeField(default=None)
    created_at = models.DateTimeField(default=None)
    start_url = models.URLField(max_length=500, default=None)
    join_url = models.URLField(max_length=200, default=None)
    meeting_code = models.CharField(max_length=30, default=None)
    meeting_password = models.CharField(max_length=30, default=None)

    def __str__(self):
        return f"idVideoconferenciaIndivual: {self.idVideoconferenciaIndivual} - idTutoriaIndividual: {self.idTutoriaIndividual} - topic: {self.topic}"


class VideoconferenciasGrupales(models.Model):
    idVideoconferenciaGrupal = models.AutoField(primary_key=True)
    idTutoriaGrupal = models.ForeignKey(
        TutoriaGrupal, on_delete=models.CASCADE)
    topic = models.CharField(max_length=80)
    start_time = models.DateTimeField(default=None)
    created_at = models.DateTimeField(default=None)
    start_url = models.URLField(max_length=500, default=None)
    join_url = models.URLField(max_length=200, default=None)
    meeting_code = models.CharField(max_length=30, default=None)
    meeting_password = models.CharField(max_length=30, default=None)

    def __str__(self):
        return f"idVideoconferenciaGrupal: {self.idVideoconferenciaGrupal} - idTutoriaGrupal: {self.idTutoriaGrupal} - topic: {self.topic}"


class Chat(models.Model):
    idChat = models.AutoField(primary_key=True)
    idTutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    idTutorado = models.ForeignKey(Tutorado, on_delete=models.CASCADE)
    mensajes_no_leidos_tutor = models.IntegerField(default=0)
    mensajes_no_leidos_tutorado = models.IntegerField(default=0)

    def __str__(self):
        return f"idChat: {self.idChat} - idTutor: {self.idTutor} - idTutorado: {self.idTutorado}"


class Mensaje(models.Model):
    idMensaje = models.AutoField(primary_key=True)
    idChat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    tutorEnvia = models.BooleanField(
        default=False, null=False)
    contenido = models.TextField(max_length=1000)
    fecha_envio = models.DateTimeField(auto_now_add=True)


class TokenZoom(models.Model):
    idTokenZoom = models.AutoField(primary_key=True)
    accessToken = models.CharField(max_length=1000)
    tipoToken = models.CharField(max_length=10)
    fechaCreado = models.DateTimeField()
    fechaExpira = models.DateTimeField()

    def __str__(self):
        return f"idTokenZoom: {self.idTokenZoom}"
