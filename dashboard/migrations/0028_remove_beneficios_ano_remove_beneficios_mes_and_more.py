# Generated by Django 4.2.4 on 2023-09-07 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_rename_total_meses_horas_auxiliarcalculo_total_meses_calendario_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='beneficios',
            name='ano',
        ),
        migrations.RemoveField(
            model_name='beneficios',
            name='mes',
        ),
        migrations.AddField(
            model_name='beneficios',
            name='funcionario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.colaboradores'),
            preserve_default=False,
        ),
    ]
