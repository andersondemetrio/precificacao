# Generated by Django 4.2.4 on 2023-09-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_remove_beneficios_funcionario_beneficios_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='descricaoobra',
            name='orcamento_id',
            field=models.CharField(max_length=100),
        ),
    ]
