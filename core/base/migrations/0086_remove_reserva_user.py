# Generated by Django 4.2 on 2023-05-11 03:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0085_alter_reserva_lector_alter_reserva_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='user',
        ),
    ]
