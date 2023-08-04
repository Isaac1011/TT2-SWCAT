from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

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
        # Llama al método save() de la clase padre para manejar el guardado del objeto
        super(Tutor, self).save(*args, **kwargs)

        # Después del guardado, convierte la contraseña en un hash seguro
        if self.password:
            self.password = make_password(self.password)

    def __str__(self):
        return f'{self.nombre} {self.apellidoPaterno} {self.apellidoMaterno}'
