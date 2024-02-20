# Generated by Django 4.2.3 on 2023-11-14 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_alter_ticket_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='tecnico',
            name='correo_tec',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='estatus',
            field=models.CharField(choices=[('Abierta', 'Abierta'), ('Esperando su respuesta', 'Esperando su respuesta'), ('Resuelta', 'Resuelta')], default='Abierta', max_length=25),
        ),
    ]