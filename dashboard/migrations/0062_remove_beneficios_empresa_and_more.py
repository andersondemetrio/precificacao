# Generated by Django 4.2.4 on 2023-10-24 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0061_merge_20231024_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficios',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='calendariomensal',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='cargos',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='colaboradores',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='descricaoobra',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='despesasdinamicas',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='empresa',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='endereco',
            name='empresa_endereco',
        ),
        migrations.RemoveField(
            model_name='gastosfixos',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='gastosvariaveis',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='propostas',
            name='empresa',
        ),
        migrations.RemoveField(
            model_name='rubrica',
            name='empresa',
        ),
    ]