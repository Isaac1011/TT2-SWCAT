# Generated by Django 4.2.4 on 2023-12-04 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0018_chat_mensaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='tutorEnvia',
            field=models.BooleanField(default=False),
        ),
    ]