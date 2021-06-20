from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from app.payments import PAGARME_API_KEY, PAGARME_ENCRYPTION_KEY
from app.payments.models import Subscription, Transaction
from app.payments.serializers import PagarmeTransactionSerializer

from rest_framework.exceptions import ValidationError

from pprint import pprint
import pagarme

pagarme.authentication_key(PAGARME_API_KEY)
User = get_user_model()


def create_plan(name, amount, days, trial_days=0, payment_methods=["credit_card"], installments=1):

    plan_data = {
        "amount": str(amount),
        "days": str(days),
        "trial_days": str(trial_days),
        "name": name,
        "payment_methods": payment_methods,
        "installments": installments
    }

    plan = pagarme.plan.create(plan_data)
    return plan


def find_plans(id):
    if len(pagarme.plan.find_all()) == 0:
        create_plan(name="Plano Standard with Trial",
                    amount=690, days=30, trial_days=7)  # 590624
        create_plan(name="Plano Standard",
                    amount=690, days=30)  # 590625

    if id:
        return pagarme.plan.find_by({"id": str(id)})
    else:
        return pagarme.plan.find_all()


def create_subscription(user_id, plan_id="590625", payment_method="credit_card"):
    print('=================== PAGARME ====================')
    user = get_object_or_404(User, pk=user_id)
    pprint(user.__dict__)
    payment_data = user.payment.all()[0]
    card_id = payment_data.card_id
    address = payment_data.address.all()[0]
    pprint(address.__dict__)
    if len(user.clients.all()) == 0:
        plan_id = "590624"

    subscription = pagarme.subscription.create({
        "card_id": card_id,
        "customer": {
            "email": user.email,
            "name": user.name,
            "document_number": user.cpf,
            "address": {
                "zipcode": address.cep,
                "neighborhood": address.neighborhood,
                "street": address.street,
                "street_number": address.number
            },
            "phone": {
                "number": user.phone[2:],
                "ddd": user.phone[:2]
            }
        },
        "payment_method": payment_method,
        "plan_id": plan_id,
        "soft_descriptor": "POSTBAKER",
        "postback_url": "http://filipelopes.me"
    })

    subscription_status_map = {
        'trialing': 'TRIAL',
        'paid': 'PAID',
        'unpaid': 'UNPAID',
        'ended': 'ENDED',
        'canceled': 'CANCELED',
    }

    transaction_status_map = {
        'processing': 'PROCESSING',
        'authorized': 'AUTHORIZED',
        'paid': 'PAID',
        'refunded': 'REFUNDED',
        'waiting_payment': 'WAITING_PAYMENT',
        'pending_refund': 'PENDING_REFUND',
        'refused': 'REFUSED'
    }

    try:
        subscription_id = subscription['id']
        # https://pagar.me/customers/#/subscriptions/{subscription_id}?token={subscription_token}
        subscription_token = subscription['manage_token']
        subscription_status = subscription_status_map[subscription['status']]
        if subscription['current_transaction']:
            transaction_id = subscription['current_transaction']['id']
            transaction_price = int(subscription['plan']['amount'])/100
            transaction_status = transaction_status_map[subscription['status']]
        customer_id = subscription['customer']['id']
        plan_id = subscription['plan']['id']
    except Exception as e:
        print(e)
        raise ValidationError(
            detail='Erro no processamento de pagamento, veritifique dados do cartão de crédito ou usuários com CPF duplicados')

    if user.pagarme_customer_id != customer_id:
        user.pagarme_customer_id = customer_id
        user.save()

    subscription_instance = Subscription(pagarme_id=subscription_id, pagarme_plan_id=plan_id,
                                         status=subscription_status, pagarme_token=subscription_token, user=user)
    subscription_instance.save()
    if subscription['current_transaction']:
        transaction_instance = Transaction(
            pagarme_id=transaction_id, price=transaction_price, status=transaction_status, subscription=subscription_instance)
        transaction_instance.save()

    return subscription_instance


def get_subscriptions(user_id: int):
    pass


def get_transactions(user_id: int):
    print('=================== GET TRANSACTIONS ====================')
    print(user_id)
    subscriptions = Subscription.objects.filter(user__id=user_id).all()
    transactions = []
    for subscription in subscriptions:
        subscription_pagarme = pagarme.subscription.find_by(
            {"id": subscription.pagarme_id})

        subscription_transactions = []
        for pagarme_transaction in pagarme.subscription.transactions(subscription.pagarme_id):
            transaction = {}
            transaction['pagarme_id'] = pagarme_transaction['id']
            transaction['price'] = int(pagarme_transaction['paid_amount'])/100
            transaction['status'] = pagarme_transaction['status'].upper()
            transaction['created_at'] = pagarme_transaction['date_created']
            transaction['subscription'] = {}
            transaction['subscription']['pagarme_id'] = subscription_pagarme[0]['id']
            transaction['subscription']['pagarme_plan_id'] = subscription_pagarme[0]['plan']['id']
            transaction['subscription']['status'] = subscription_pagarme[0]['status'].upper()
            transaction['subscription']['created_at'] = subscription_pagarme[0]['date_created']
            subscription_transactions.append(transaction)
        
        transactions.append(subscription_transactions)
    return transactions


def cancel_subscription(subscription_id: int):
    subscription_instance = Subscription.objects.get(pagarme_id=subscription_id)
    subscription = pagarme.subscription.cancel(subscription_id)
    subscription_instance.status = subscription['status'].upper()
    subscription_instance.save()
    return subscription
