# Generated by Django 4.2.4 on 2023-08-09 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0006_alter_tutorado_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutoriaindividual',
            name='idTutoriaIndividual',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
