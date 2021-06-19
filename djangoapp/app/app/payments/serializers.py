from rest_framework import serializers
from app.payments.models import Transaction, Subscription


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class PagarmeSubscriptionSerializer(serializers.Serializer):
    # https://www.django-rest-framework.org/api-guide/fields
    pagarme_id = serializers.IntegerField()
    pagarme_plan_id = serializers.IntegerField()
    status = serializers.ChoiceField(choices=Subscription.STATUS_CHOICES)
    created_at = serializers.DateTimeField()


class PagarmeTransactionSerializer(serializers.Serializer):
    pagarme_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    status = serializers.ChoiceField(choices=Transaction.STATUS_CHOICES)
    subscription = PagarmeSubscriptionSerializer(required=True)
    created_at = serializers.DateTimeField()
