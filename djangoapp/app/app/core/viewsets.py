from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action

from app.core.permissions import IsAdminOrIsSelf
from app.core.models import Address, Payment
from app.core.serializers import SimplifiedUserSerializer, UserSerializer, CreateUserSerializer, GroupSerializer, AddressSerializer, PaymentSerializer
from app.core.exceptions import UniqueEmail
from app.payments.utils import get_transactions
from app.payments.models import Transaction
from app.payments.serializers import PagarmeTransactionSerializer

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
            payment_data = request.data['payment'][0]
            request.data.pop('payment')
            address_data = payment_data.pop('address')[0]
            user = User(**request.data)
            user.set_password(request.data.get('password', None))
            user.save()
            payment = Payment(**payment_data)
            payment.save()
            user.payment.set([payment])
            address = Address(**address_data)
            address.save()
            payment.address.set([address])
            serializer = UserSerializer(
                user, many=False, context={'request': request})
            return Response(serializer.data)
        except IntegrityError as e:
            raise UniqueEmail(
                detail=f"email {request.data['email']} already exists, {e}")

    def partial_update(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        try:
            if 'password' in request.data:
                user.set_password(request.data.get('password', None))
                user.save()
            if 'payment' in request.data:
                payment_data = request.data['payment'][0]
                request.data.pop('payment')
                if 'address' in payment_data:
                    address_data = payment_data['address'][0]
                    payment = Payment.objects.get(user_id=pk)
                    Address.objects.filter(
                        payment_id=payment.id).update(**address_data)
                    payment_data.pop('address')
                Payment.objects.filter(user_id=pk).update(**payment_data)
            # Email não é editável
            if 'email' in request.data:
                request.data.pop('email')
            User.objects.filter(pk=pk).update(**request.data)
            serializer = UserSerializer(
                user, many=False)
            return Response(serializer.data)
        except IntegrityError as e:
            raise UniqueEmail(
                detail=f"IntegrityError: {e}")

    def update(self, request, *args, **kwargs):
        return self.partial_update(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs.get('pk', None)
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(
            user, many=False, context={'request': request})
        return Response(serializer.data)

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
        if self.action == 'create':
            return CreateUserSerializer
        else:
            return UserSerializer

    @action(methods=["get"], detail=True, url_path="transactions", name="user_transactions")
    def user_transactions(self, request, *args, **kwargs):
        transactions = get_transactions(request.user.id)
        serializer = PagarmeTransactionSerializer(
            transactions, many=True)
        return Response(serializer.data)


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
