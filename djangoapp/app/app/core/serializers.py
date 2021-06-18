from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.fields import EmailField

from rest_framework import serializers

from app.core.models import Payment, Address
from app.clients.models import Client
from app.clients.serializers import CreateClientSerializer


class SimplifiedUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'url', 'email', 'name', 'cpf', 'phone']


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['cep', 'street', 'number',
                  'city', 'state_uf', 'neighborhood']


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer(many=True)

    class Meta:
        model = Payment
        fields = ['address', 'card_id']
        depth = 2


class UserSerializer(serializers.HyperlinkedModelSerializer):
    payment = PaymentSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'cpf', 'phone', 'payment']
        depth = 2


class CreateUserSerializer(serializers.HyperlinkedModelSerializer):
    payment = PaymentSerializer(many=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name', 'cpf', 'phone', 'payment']
        depth = 2

    def create(self, validated_data):
        payment = validated_data.pop('payment')
        client = validated_data.pop('client')
        user = self.model.objects.create(**validated_data)
        address = payment_data.pop('address')
        payment = Payment.objects.create(user=user, **payment)
        address = Address.objects.create(
            payment=payment_instance, **address)
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserRecoverPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
