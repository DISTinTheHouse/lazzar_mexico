# Generated by Django 4.2.3 on 2023-09-12 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('almacen', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codigo_almacen',
            old_name='codigo_almacen',
            new_name='cod_almacen',
        ),
    ]
