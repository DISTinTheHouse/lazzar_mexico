# Generated by Django 4.2.6 on 2024-02-01 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_correoslazzar_num_empleado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='correoslazzar',
            name='num_empleado',
        ),
    ]