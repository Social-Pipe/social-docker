from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.clients.models import Client
from app.clients.serializers import ClientSerializer

from pprint import pprint

User = get_user_model()


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed or edited.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=["get"], detail=True, url_path="posts", url_name="posts")
    def get_posts(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, request):
        pprint(request.data)
        client = Client(**request.data)
        client.password = make_password(request.data.get('password', None))
        client.access_hash = get_random_string(length=16)
        user = User.objects.get(pk=request.user.id)
        client.user = user
        client.save()
        serializer = ClientSerializer(client, many=False, context={'request': request})
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
