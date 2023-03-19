# Generated by Django 4.1.7 on 2023-03-19 16:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_alter_libro_f_publicacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('tipoEvento', models.CharField(max_length=50)),
                ('fecha', models.DateTimeField(default=datetime.datetime.now, verbose_name='Fecha y Hora')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('imagen', models.ImageField(blank=True, max_length=255, null=True, upload_to='Eventos/', verbose_name='Imagen')),
            ],
        ),
        migrations.AlterField(
            model_name='autor',
            name='descripcion',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='f_publicacion',
            field=models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Publicación'),
        ),
        migrations.AlterField(
            model_name='productos',
            name='categoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.categoria', verbose_name='Categoría'),
        ),
        migrations.AlterField(
            model_name='productos',
            name='pvp',
            field=models.DecimalField(decimal_places=0, default=0.0, max_digits=9, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='productos',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Cantidad o Stock'),
        ),
    ]
