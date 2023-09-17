# Generated by Django 4.2.4 on 2023-09-17 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_rubrica_valor_sugerido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descricaoobra',
            name='custo_hora_con',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='descricaoobra',
            name='custo_mod',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='descricaoobra',
            name='custo_total',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]