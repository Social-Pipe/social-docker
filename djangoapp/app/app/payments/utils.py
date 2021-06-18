from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from app.payments import PAGARME_API_KEY, PAGARME_ENCRYPTION_KEY
from app.payments.models import Subscription, Transaction

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

    pprint(subscription)
    try:
        subscription_id = subscription['id']
        # https://pagar.me/customers/#/subscriptions/{subscription_id}?token={subscription_token}
        subscription_token = subscription['manage_token']
        subscription_status = 'OPENED' if subscription['status'] == 'paid' else 'CANCELED'
        transaction_id = subscription['current_transaction']['id']
        transaction_price = int(subscription['plan']['amount'])/100
        transaction_status = 'PAID' if subscription['status'] == 'paid' else 'ERROR'
        customer_id = subscription['customer']['id']
        plan_id = subscription['plan']['id']
    except Exception as e:
        raise ValidationError(detail='Erro no processamento de pagamento, veritifique dados do cartão de crédito ou usuários com CPF duplicados')

    if user.pagarme_customer_id != customer_id:
        user.pagarme_customer_id = customer_id
        user.save()

    subscription_instance = Subscription(pagarme_id=subscription_id, pagarme_plan_id=plan_id,
                                         status=subscription_status, pagarme_token=subscription_token, user=user)
    subscription_instance.save()
    transaction_instance = Transaction(
        pagarme_id=transaction_id, price=transaction_price, status=transaction_status, subscription=subscription_instance)
    transaction_instance.save()

    return subscription


def get_subscription(client_id: int):
    pass


def cancel_subscription(subscription_id: int):
    subscription = pagarme.subscription.cancel("ID_DA_SUBSCRIPTION")
