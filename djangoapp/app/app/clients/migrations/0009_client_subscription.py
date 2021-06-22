# Generated by Django 3.1.12 on 2021-06-19 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20210619_1825'),
        ('clients', '0008_auto_20210617_2141'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.subscription'),
        ),
    ]
