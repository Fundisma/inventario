# Generated by Django 4.2 on 2023-04-20 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0071_alter_eventos_estado_alter_productos_estado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='fecha_creacion',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]