# Generated by Django 4.2.4 on 2023-08-26 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_calendariomensal_jornada_diaria'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setor', models.CharField(choices=[('Prestador de Serviço', 'Prestador de Serviço'), ('Gestores', 'Gestores')], max_length=50)),
                ('cargo', models.CharField(choices=[('Auxiliar', 'Auxiliar'), ('Assistente Técnico', 'Assistente Técnico'), ('Técnico N1', 'Técnico N1'), ('Técnico N2', 'Técnico N2'), ('Técnico N3', 'Técnico N3'), ('Coordenador', 'Coordenador'), ('Gerente', 'Gerente'), ('Diretor', 'Diretor')], max_length=50)),
                ('periculosidade', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fgts', models.DecimalField(decimal_places=2, max_digits=10)),
                ('um_terco_ferias', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fgts_ferias', models.DecimalField(decimal_places=2, max_digits=10)),
                ('decimo_terceiro', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fgts_decimo_terceiro', models.DecimalField(decimal_places=2, max_digits=10)),
                ('multa_rescisoria', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rateio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('custo_mes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.colaboradores')),
            ],
        ),
    ]
