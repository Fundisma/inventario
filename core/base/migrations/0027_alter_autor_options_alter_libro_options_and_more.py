# Generated by Django 4.1.6 on 2023-03-11 01:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_alter_libro_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'ordering': ['id'], 'verbose_name': 'Autor', 'verbose_name_plural': 'Autores'},
        ),
        migrations.AlterModelOptions(
            name='libro',
            options={'ordering': ['id'], 'verbose_name': 'Libro', 'verbose_name_plural': 'Libros'},
        ),
        migrations.AlterField(
            model_name='libro',
            name='f_publicacion',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
