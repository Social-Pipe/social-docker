from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseMultiPartParser, CamelCaseJSONParser

from app.clients.models import Client, Post, PostFile, Comment
from app.clients.serializers import ClientSerializer, CreateClientSerializer, PostSerializer, CreatePostSerializer, PostFileSerializer, CommentSerializer, CreatePostFileSerializer
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
    # permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [CamelCaseFormParser, CamelCaseMultiPartParser]
    lookup_field = 'access_hash'

    @action(methods=["get", "post"], detail=True, url_path="posts", name="client_posts")
    def client_posts(self, request, *args, **kwargs):
        if hasattr(request, 'client'):
            client = request.client
        else:
            client = get_object_or_404(
                Client, access_hash=kwargs.get('access_hash', None))
        if request.method == 'GET':
            print(client)
            posts = Post.objects.filter(client=client)
            serializer = PostSerializer(
                posts, many=True, context={'request': request})
            return Response(serializer.data)
        elif request.method == 'POST':
            post = Post(**request.data)
            post.client = client
            post.save()
            serializer = PostSerializer(
                post, many=False, context={'request': request})
            return Response(serializer.data)

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
            queryset = Post.objects.all()
        elif self.action == 'list':
            queryset = Client.objects.filter(user=self.request.user).all()

        return queryset

    def get_parsers(self):
        if self.action_map['get'] == 'client_posts':
            parser_classes = [CamelCaseJSONParser]
        else:
            parser_classes = [CamelCaseFormParser, CamelCaseMultiPartParser]
        return [parser_class() for parser_class in parser_classes]

    def get_serializer_class(self):
        """
        Instantiates and returns the list of serializers that this view requires.
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CreateClientSerializer
        elif self.action == 'client_posts' and self.request.method == 'POST':
            return CreatePostSerializer
        elif self.action == 'client_posts' and self.request.method == 'GET':
            return PostSerializer
        else:
            return ClientSerializer

    def get_permissions(self):
        if self.action == 'client_posts' and self.request.method == 'GET':
            permission_classes = [IsAuthenticatedOrIsClient]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostFileViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    # serializer_class = PostFileSerializer
    permission_classes = [IsAuthenticatedOrIsClient]

    def get_serializer_class(self):
        """
        Instantiates and returns the list of serializers that this view requires.
        """
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CreatePostFileSerializer
        else:
            return ClientSerializer

    def get_parsers(self):
        if self.action == 'list' or self.action == 'retrieve':
            parser_classes = [CamelCaseJSONParser]
        else:
            parser_classes = [CamelCaseFormParser, CamelCaseMultiPartParser]
        return [parser_class() for parser_class in parser_classes]


class CommentViewSet(viewsets.ModelViewSet):
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
