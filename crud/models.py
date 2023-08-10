from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Tutor(models.Model):
    idTutor = models.AutoField(primary_key=True)
    numeroEmpleado = models.CharField(max_length=7, unique=True)
    email = models.CharField(max_length=45, unique=True)
    password = models.CharField(max_length=128)
    nombre = models.CharField(max_length=45)
    apellidoPaterno = models.CharField(max_length=45)
    apellidoMaterno = models.CharField(max_length=45)
    cubiculo = models.CharField(max_length=20, default=None)
    telefono = models.CharField(max_length=10, default=None)

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
    semestre = models.CharField(max_length=15, default=None)
    telefono = models.CharField(max_length=10, default=None)
    numTutoresAsignados = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(3)])

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
