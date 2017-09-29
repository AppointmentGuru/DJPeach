'''Various utils to make testing easier'''

from ..models import CreditCard, Transaction, Product
from django.contrib.auth import get_user_model
from faker import Factory
from .datas import SUCCESS_PAYMENT
import random, uuid, json

FAKE = Factory.create()

def get_uuid():
    return str(uuid.uuid4())

def create_user():
    return get_user_model().objects.create_user(
        username=FAKE.user_name(),
        email=FAKE.email(),
        password='testtest'
    )

def create_product(**kwargs):
    data = {
        'currency': 'ZAR',
        'price': FAKE.numerify(),
        'title': FAKE.sentence(),
        'is_recurring': FAKE.boolean(),
        'recurrance_rate': random.choice(['M','A'])
    }
    data.update(kwargs)
    return Product.objects.create(**data)

def create_card(user, **kwargs):

    data = {
        "user": user,
        "cardholder_name": FAKE.name(),
        "registration_id": get_uuid(),
        "bin": get_uuid(),
        "expiry_month": FAKE.credit_card_expire().split('/')[0],
        "expiry_year": FAKE.credit_card_expire().split('/')[1],
        "last_four_digits": FAKE.credit_card_number()[-4:],
    }
    data.update(kwargs)
    return CreditCard.objects.create(**data)

def create_transaction():
    data = SUCCESS_PAYMENT
    transaction = {
        # "user_id": user.id,
        "currency": data.get('currency'),
        "price": data.get('amount'),
        "transaction_id": data.get('id'),
        "ndc": data.get('ndc'),
        "payment_brand": data.get('paymentBrand'),
        "payment_type": data.get('paymentType'),
        "registration_id": data.get('registrationId'),
        "result_code": data.get('result', {}).get('code'),
        "result_description": data.get('result', {}).get('description'),
        "data": json.dumps(data)
    }
    return Transaction.objects.create(**transaction)