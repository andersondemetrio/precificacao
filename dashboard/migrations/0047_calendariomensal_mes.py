# Generated by Django 4.2.4 on 2023-09-22 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0046_remove_calendariomensal_funcionario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendariomensal',
            name='mes',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
