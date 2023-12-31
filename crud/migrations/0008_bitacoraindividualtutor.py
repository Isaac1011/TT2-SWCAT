# Generated by Django 4.2.4 on 2023-08-11 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0007_alter_tutoriaindividual_idtutoriaindividual'),
    ]

    operations = [
        migrations.CreateModel(
            name='BitacoraIndividualTutor',
            fields=[
                ('idBitacoraIndividual', models.AutoField(primary_key=True, serialize=False)),
                ('nota', models.CharField(max_length=400)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('idTutoriaIndividual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crud.tutoriaindividual')),
            ],
        ),
    ]
