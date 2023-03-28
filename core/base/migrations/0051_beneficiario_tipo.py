# Generated by Django 4.1.7 on 2023-03-20 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0050_remove_productos_tipobeneficio_productos_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiario',
            name='tipo',
            field=models.CharField(choices=[('Funcionario', 'Funcionario'), ('Beneficiario', 'Beneficiario')], default='Funcionario', max_length=25, verbose_name='Tipo'),
        ),
    ]