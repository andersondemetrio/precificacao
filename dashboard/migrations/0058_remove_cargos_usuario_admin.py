# Generated by Django 4.2.4 on 2023-10-24 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0057_cargos_usuario_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargos',
            name='usuario_admin',
        ),
    ]
