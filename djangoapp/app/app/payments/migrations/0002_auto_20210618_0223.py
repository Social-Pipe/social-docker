# Generated by Django 3.1.12 on 2021-06-18 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('PAID', 'Pago'), ('ERROR', 'Erro')], default='PAID', max_length=9),
        ),
    ]
