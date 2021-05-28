from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from app.core.models import Payment, Address
from rest_framework import serializers


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
    address = AddressSerializer(many=False)

    class Meta:
        model = Payment
        fields = ['address', 'card_id']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    payment = PaymentSerializer(many=False)

    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'cpf', 'phone', 'payment']
        depth = 2

    def create(self, validated_data):
        print('validated_data')
        print(validated_data)
        payment_data = validated_data
        user = self.model.objects.create(**validated_data)
        address_data = payment_data.pop('address')
        payment_instance = Payment.objects.create(user=user, **payment_data)
        address_instance = Address.objects.create(
            payment=payment_instance, **address_data)
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
