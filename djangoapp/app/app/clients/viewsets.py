from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseMultiPartParser

from app.clients.models import Client, Post, PostFile, Comment
from app.clients.serializers import ClientSerializer, CreateClientSerializer, PostSerializer, PostFileSerializer, CommentSerializer
from app.clients.permissions import IsAuthenticatedOrIsClient

import json
from pprint import pprint

User = get_user_model()


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed or edited.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [CamelCaseFormParser, CamelCaseMultiPartParser]
    lookup_field = 'access_hash'

    @action(methods=["get"], detail=True, url_path="posts", url_name="posts")
    def get_posts(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request):
        logo = request.data['logo']
        client = Client(**request.data)
        client.name = request.data['name']
        client.facebook = json.loads(request.data['facebook'])
        client.instagram = json.loads(request.data['instagram'])
        client.linkedin = json.loads(request.data['linkedin'])
        client.logo = default_storage.save(
            f"client/logo/{logo.name}", ContentFile(logo.read()))
        client.password = make_password(request.data.get('password', None))
        client.access_hash = get_random_string(length=16)
        user = User.objects.get(pk=request.user.id)
        client.user = user
        client.save()
        # 
        # 
        # Realizar pagamento junto à pagarme
        # 
        # 
        serializer = ClientSerializer(
            client, many=False, context={'request': request})
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.queryset

        if self.action == 'get_posts':
            queryset = self.queryset
        elif self.action == 'list':
            queryset = Client.objects.filter(user=self.request.user).all()

        return queryset

    def get_serializer_class(self):
        """
        Instantiates and returns the list of serializers that this view requires.
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CreateClientSerializer
        else:
            return ClientSerializer

class Post(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    '''
    ?facebook=true&...
    '''

class PostFile(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostFileSerializer
    permission_classes = [IsAuthenticatedOrIsClient]

class Comment(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrIsClient]

'''
/client-token
hash
password
isAuthenticatedOrIsClient
verificar se tem reques.user, senão verifica por outro token e se tem scope client no payload e sub (subject) o hash do cliente
se não, False
'''