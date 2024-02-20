# Generated by Django 4.2.3 on 2023-07-14 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CorreosLazzar',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('correo', models.EmailField(max_length=200, verbose_name='Correo')),
                ('esvendedor', models.BooleanField(verbose_name='Es Vendedor?')),
            ],
            options={
                'verbose_name': 'Correo',
                'verbose_name_plural': 'Correos',
            },
        ),
    ]