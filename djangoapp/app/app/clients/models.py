from django.db import models
from django.contrib.auth import get_user_model
from app.payments.models import Subscription

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
        get_user_model(), related_name='clients', on_delete=models.CASCADE, blank=True, null=True)
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}@{self.access_hash}"

class Post(models.Model):
    TYPE_CHOICES = (
        ("SINGLE", "Única Imagem"),
        ("VIDEO", "Único vídeo"),
        ("GALLERY", "Diversos, vídeos ou imagens")
    )

    STATUS_CHOICES = (
        ("NONE", "Ainda não avaliada"),
        ("APPROVED", "Aprovada"),
        ("ATTENTION", "Carece de atenção para alterações"),
        ("CANCELED", "Cancelada"),
    )

    instagram = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)
    linkedin = models.BooleanField(default=False)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, blank=False, null=False, default="SINGLE")
    caption = models.TextField()
    posting_date = models.DateTimeField()
    publish = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, blank=False, null=False, default="NONE")
    client  = models.ForeignKey(
        'Client', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption

class PostFile(models.Model):
    file = models.FileField(upload_to='client/files/', null=True, blank=True)
    order = models.IntegerField(default=1)
    post  = models.ForeignKey(
        'Post', related_name='files', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    WRITER_CHOICES = (
        ("USER", "Usuário"),
        ("CLIENT", "Cliente do usuário"),
    )

    writer = models.CharField(max_length=6, choices=WRITER_CHOICES, blank=False, null=False)
    message = models.TextField()
    post  = models.ForeignKey(
        'Post', related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
