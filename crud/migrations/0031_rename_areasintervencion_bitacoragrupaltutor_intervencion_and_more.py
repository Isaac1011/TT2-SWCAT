# Generated by Django 4.2.4 on 2023-12-20 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0030_bitacoragrupaltutor_areasintervencion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bitacoragrupaltutor',
            old_name='areasIntervencion',
            new_name='intervencion',
        ),
        migrations.RenameField(
            model_name='bitacoraindividualtutor',
            old_name='areasIntervencion',
            new_name='intervencion',
        ),
    ]
