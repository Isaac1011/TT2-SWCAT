# Generated by Django 4.2.4 on 2023-12-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0020_tutor_acepta_terminos_tutorado_acepta_terminos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='cubiculo',
            field=models.CharField(default=None, max_length=50),
        ),
        migrations.AlterField(
            model_name='tutoriagrupal',
            name='salon',
            field=models.CharField(default=None, max_length=50),
        ),
    ]
