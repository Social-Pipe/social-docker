from django.db import models
from django.contrib.auth import get_user_model


class Transaction(models.Model):
    STATUS_CHOICES = (
        ("PAID", "Pago"),
        ("ERROR", "Erro"),
    )

    pagarme_id = models.PositiveBigIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, blank=False, null=False, default="PAID")
    subscription = models.ForeignKey(
        'Subscription', related_name='transactions', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Subscription(models.Model):
    STATUS_CHOICES = (
        ("OPENED", "Aberta"),
        ("CANCELED", "Cancelada"),
    )

    pagarme_id = models.PositiveBigIntegerField()
    pagarme_plan_id = models.PositiveBigIntegerField()
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, blank=False, null=False, default="OPENED")
    pagarme_token = models.CharField(max_length=128)
    user = models.ForeignKey(
        get_user_model(), related_name='subscriptions', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
