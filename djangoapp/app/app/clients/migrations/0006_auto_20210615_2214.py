# Generated by Django 3.1.12 on 2021-06-15 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_auto_20210615_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfile',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='client/files/'),
        ),
    ]
