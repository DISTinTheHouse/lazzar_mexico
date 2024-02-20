# Generated by Django 4.2.3 on 2023-11-14 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='estatus',
            field=models.CharField(choices=[('Abierta', 'Abierta'), ('Esperando', 'Esperando su respuesta'), ('Resuelta', 'Resuelta')], default='Abierta', max_length=25),
        ),
    ]