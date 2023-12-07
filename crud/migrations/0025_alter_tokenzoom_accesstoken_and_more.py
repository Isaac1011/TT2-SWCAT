# Generated by Django 4.2.4 on 2023-12-07 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0024_tokenzoom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tokenzoom',
            name='accessToken',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='tokenzoom',
            name='fechaCreado',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='tokenzoom',
            name='fechaExpira',
            field=models.DateTimeField(),
        ),
    ]