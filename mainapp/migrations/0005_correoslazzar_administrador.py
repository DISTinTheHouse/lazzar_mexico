# Generated by Django 4.2.3 on 2023-08-22 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_alter_correoslazzar_vender_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='correoslazzar',
            name='administrador',
            field=models.BooleanField(default=False, verbose_name='Es Administrador?'),
        ),
    ]
