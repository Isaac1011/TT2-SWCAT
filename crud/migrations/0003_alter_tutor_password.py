# Generated by Django 4.2.4 on 2023-08-02 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
