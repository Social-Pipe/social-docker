from django.conf import settings
from django.contrib.auth.hashers import check_password

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from app.clients.serializers import ClientObtainTokenSerializer
from app.clients.models import Client

import jwt
import datetime


class ClientToken(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ClientObtainTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Captura o cliente pelo hash
        client = Client.objects.get(
            access_hash=request.data.get('access_hash', None))
        # Verifica se a senha coincide
        if check_password(request.data.get('password', None), client.password):
            encoded_jwt = jwt.encode({
                "token_type": "access",
                "sub": client.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
                "scope": "client"
            }, settings.SECRET_KEY, algorithm="HS256")
            return Response({"access_token": encoded_jwt}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied(detail="Incorrect hash/password", code=None)
