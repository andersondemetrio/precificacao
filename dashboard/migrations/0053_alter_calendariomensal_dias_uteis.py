# Generated by Django 4.2.4 on 2023-09-25 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0052_alter_calendariomensal_dias_uteis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendariomensal',
            name='dias_uteis',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]