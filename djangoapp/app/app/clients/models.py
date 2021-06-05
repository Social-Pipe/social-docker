from django.db import models
from django.contrib.auth import get_user_model


class Client(models.Model):
    logo = models.ImageField(upload_to='client/logo/', null=True, blank=True)
    name = models.CharField(max_length=128)
    access_hash = models.CharField(
        max_length=64, help_text="Hash curto para link de acesso", unique=True)
    password = models.CharField(max_length=128, help_text="Hashed password")
    instagram = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)
    linkedin = models.BooleanField(default=False)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

