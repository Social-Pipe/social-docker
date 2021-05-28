# Generated by Django 3.1.11 on 2021-05-28 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='client/logo/')),
                ('name', models.CharField(max_length=128)),
                ('access_hash', models.CharField(help_text='Hash curto para link de acesso', max_length=64)),
                ('password', models.CharField(help_text='Hashed password', max_length=128)),
                ('instagram', models.BooleanField(default=False)),
                ('facebook', models.BooleanField(default=False)),
                ('linkedin', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
