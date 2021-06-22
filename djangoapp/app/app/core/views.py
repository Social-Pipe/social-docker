from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from app.core.serializers import UserRecoverPasswordSerializer

import jwt
import datetime
User = get_user_model()


class RecoverPassword(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRecoverPasswordSerializer

    def post(self, request):
        # Verifica se o usuário de fato existe
        email = request.data['email']
        user = get_object_or_404(User, email=email)
        # Atualizando senha
        new_password = get_random_string(length=12)
        user.set_password(new_password)
        user.save()
        # Envia email
        send_mail(
            'Recuperação de senha',
            f'''Olá {user.name},

            Você solicitou uma recuperação de senha. Se não foi o caso, por favor reporte à administração. Sua nova senha é:

            {new_password}

            Você pode modificar essa nova senha na página de configurações do Postbaker.

            Equipe Postbaker.''',
            'naoresponda@filipelopes.me',
            [user.email],
            fail_silently=False,
        )
        return Response({"detail": "Message sent"}, status=status.HTTP_200_OK)
