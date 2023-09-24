# Generated by Django 4.2.4 on 2023-09-23 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0049_remove_rubrica_alimentacao_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DespesasDinamicas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rubrica_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.rubrica')),
            ],
        ),
        migrations.RemoveField(
            model_name='gastosvariaveis',
            name='insumo',
        ),
        migrations.DeleteModel(
            name='Insumos',
        ),
    ]
