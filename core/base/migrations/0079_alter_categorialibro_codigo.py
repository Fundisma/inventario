# Generated by Django 4.2 on 2023-04-27 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0078_alter_categorialibro_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorialibro',
            name='codigo',
            field=models.CharField(max_length=3, null=True, unique=True, verbose_name='Codigo'),
        ),
    ]