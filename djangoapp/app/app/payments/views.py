from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth.models import User

class ListenSubscriptionStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pagarme_subscription_id, format=None):
        print(f'Atualizado status de subscription {pagarme_subscription_id}')
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)