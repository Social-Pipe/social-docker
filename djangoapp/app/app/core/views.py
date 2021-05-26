from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.core.permissions import IsAdminOrIsSelf
from app.core.serializers import UserSerializer, CreateUserSerializer, GroupSerializer
from app.core.exceptions import UniqueEmail

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        try:
            user = User(**request.data)
            user.set_password(request.data.get('password', None))
            user.save()
            serializer = CreateUserSerializer(user, many=False)
            return Response(serializer.data)
        except IntegrityError:
            raise UniqueEmail(detail=f"email {request.data['email']} already exists")

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsAdminOrIsSelf]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """
        Instantiates and returns the list of serializers that this view requires.
        """
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# def user_logged_in(request, format=None):
#     print(request)
#     content = {
#         'user': str(request.user),  # `django.contrib.auth.User` instance.
#         'auth': str(request.auth),  # None
#     }
#     return Response(content)
