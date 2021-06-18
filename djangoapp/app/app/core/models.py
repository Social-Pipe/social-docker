from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager

# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#specifying-a-custom-user-model


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    name = models.CharField(max_length=120, blank=True)
    cpf = models.CharField(max_length=11, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    pagarme_customer_id = models.PositiveBigIntegerField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = self.name
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.name.split(',')[0]

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Address(models.Model):
    cep = models.CharField(max_length=9)
    street = models.CharField(max_length=258)
    number = models.CharField(max_length=64)
    city = models.CharField(max_length=128)
    state_uf = models.CharField(max_length=2)
    neighborhood = models.CharField(max_length=128)
    payment = models.ForeignKey(
        'Payment', related_name='address', on_delete=models.CASCADE, blank=True, null=True)


# https://docs.pagar.me/docs/realizando-uma-transacao-de-cartao-de-credito#criando-um-cart%C3%A3o-para-one-click-buy
class Payment(models.Model):
    card_id = models.CharField(max_length=64)
    user = models.ForeignKey(
        'User', related_name='payment', on_delete=models.CASCADE, blank=True, null=True)
