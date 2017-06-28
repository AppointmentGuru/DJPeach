from ..models import CreditCard, Transaction, Product
from django.contrib.auth import get_user_model
import random, uuid
from faker import Factory
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