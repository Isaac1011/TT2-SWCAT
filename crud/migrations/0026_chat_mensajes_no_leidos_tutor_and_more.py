# Generated by Django 4.2.4 on 2023-12-18 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0025_alter_tokenzoom_accesstoken_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='mensajes_no_leidos_tutor',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chat',
            name='mensajes_no_leidos_tutorado',
            field=models.IntegerField(default=0),
        ),
    ]