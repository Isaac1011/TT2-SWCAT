# Generated by Django 4.2.4 on 2023-12-07 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0023_tutorado_genero_alter_tutorado_semestre'),
    ]

    operations = [
        migrations.CreateModel(
            name='TokenZoom',
            fields=[
                ('idTokenZoom', models.AutoField(primary_key=True, serialize=False)),
                ('accessToken', models.CharField(max_length=600)),
                ('tipoToken', models.CharField(max_length=10)),
                ('fechaCreado', models.DateField()),
                ('fechaExpira', models.DateField()),
            ],
        ),
    ]
