# Generated by Django 4.2.4 on 2023-12-06 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0021_alter_tutor_cubiculo_alter_tutoriagrupal_salon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='cubiculo',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='tutoriagrupal',
            name='salon',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
