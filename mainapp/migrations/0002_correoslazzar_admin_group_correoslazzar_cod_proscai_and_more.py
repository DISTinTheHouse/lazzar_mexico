# Generated by Django 4.2.3 on 2023-07-26 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='correoslazzar',
            name='admin_group',
            field=models.BooleanField(default=False, verbose_name='Admin Grupo?'),
        ),
        migrations.AddField(
            model_name='correoslazzar',
            name='cod_Proscai',
            field=models.CharField(default='', max_length=3, verbose_name='Codigo Proscai'),
        ),
        migrations.AddField(
            model_name='correoslazzar',
            name='group_Proscai',
            field=models.CharField(default='', max_length=250, verbose_name='Grupo Proscai'),
        ),
        migrations.AddField(
            model_name='correoslazzar',
            name='nombre',
            field=models.CharField(default='', max_length=250, verbose_name='Nombre'),
        ),
    ]