# Generated by Django 4.2.4 on 2023-09-17 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0040_rubrica_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubrica',
            name='valor_sugerido',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
    ]