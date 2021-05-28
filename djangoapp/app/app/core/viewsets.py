from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from app.core.permissions import IsAdminOrIsSelf
from app.core.models import Address, Payment
from app.core.serializers import SimplifiedUserSerializer, UserSerializer, GroupSerializer, AddressSerializer, PaymentSerializer
from app.core.exceptions import UniqueEmail

from pprint import pprint

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = SimplifiedUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        try:
            pprint(request.data)
            user = User(**request.data)
            user.set_password(request.data.get('password', None))
            payment = request.data['payment']
            address = payment['address']
            payment = Payment(**payment)
            address = Address(**address)
            user.save()
            payment.user = user
            payment.save()
            address.payment = payment
            address.save()
            pprint(user.__dict__)
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        except IntegrityError:
            raise UniqueEmail(
                detail=f"email {request.data['email']} already exists")

    def retrieve(self, request, *args, **kwargs):
        print('args')
        print(args)
        print('kwargs')
        user_id = kwargs.get('pk', None)
        user = User.objects.get(pk=user_id)
        print(user)
        payment = Payment.objects.filter(user=user).first()
        print(payment)
        address = Address.objects.filter(payment=payment).first()
        payment.address = address
        user.payment = payment
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    @action(methods=["get"], detail=True, url_path="clients", url_name="clients")
    def get_clients(self, request, *args, **kwargs):
        return self.retrive(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.queryset

        if self.action == 'get_clients':
            queryset = self.queryset

        return queryset

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
        if self.action == 'list' or self.action == 'retrieve':
            return SimplifiedUserSerializer
        else:
            return UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class AddressViewSet(viewsets.ModelViewSet):
    """
    Address model is a Payment child. It stores an address payment data from an user.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.AllowAny]


class PaymentViewSet(viewsets.ModelViewSet):
    """
    Payment payment data from an user.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.AllowAny]
