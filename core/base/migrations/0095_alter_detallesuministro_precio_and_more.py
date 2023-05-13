# Generated by Django 4.2 on 2023-05-12 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0094_alter_suministro_subtotal_alter_suministro_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallesuministro',
            name='precio',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='detallesuministro',
            name='subtotal',
            field=models.DecimalField(decimal_places=3, default=0.0, max_digits=9),
        ),
    ]