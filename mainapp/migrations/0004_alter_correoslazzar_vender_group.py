# Generated by Django 4.2.3 on 2023-08-11 22:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_correoslazzar_vender_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='correoslazzar',
            name='vender_group',
            field=models.BooleanField(default=False, verbose_name='Vendedor Solo?'),
        ),
    ]
