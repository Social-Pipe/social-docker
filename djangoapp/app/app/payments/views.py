from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User
from django.conf import settings
import os


class ListenSubscriptionStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pagarme_subscription_id, format=None):
        print(f'Atualizado status de subscription {pagarme_subscription_id}')
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


class ApiKey(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        if settings.PAYMENT_ENV == 'production':
            api_key = os.environ['PAGARME_API_KEY_LIVE']
        else:
            api_key = os.environ['PAGARME_API_KEY_TEST']
        print(f'Pagarme apikey solicitada, {api_key}')

        return Response({'api_key': api_key})
