from django.conf import settings
from .models import CreditCard, Transaction

from slackclient import SlackClient
import requests, json, uuid, os

def post_to_slack(data):
    token = os.environ.get('SLACK_TOKEN', None)
    if token is not None:
        slack_client = SlackClient(token)

        channel = settings.SLACK_CHANNEL
        message = "```{}```".format(json.dumps(data, indent=2))
        res = slack_client.api_call("chat.postMessage", channel=channel, text=message)
        return res

def recurring_transaction_data_from_transaction(data):

    amount = data.get('amount')
    currency = data.get('currency')

    return {
        'authentication.userId' : settings.PEACH_USER_ID,
        'authentication.password' : settings.PEACH_PASSWORD,
        'authentication.entityId' : settings.PEACH_ENTITY_RECURRING_ID,
        "amount": amount,
        "currency": currency,
        "paymentType": "PA",
        "recurringType": "REPEATED"
    }

def prepare_checkout_data(request, user=None, product=None):
    cards = []
    # :user/:product/:transaction
    transaction_id = str(uuid.uuid4())

    data = {
        "authentication.userId": settings.PEACH_USER_ID,
        "authentication.password": settings.PEACH_PASSWORD,
        "authentication.entityId": settings.PEACH_ENTITY_RECURRING_ID,
        # "authentication.entityId": settings.PEACH_ENTITY_ID,
        "createRegistration": True,
        "paymentType": "DB",
        "recurringType": "INITIAL",
    }

    if product is not None:
        transaction_id = '{}/{}'.format(product.id, transaction_id)
        price = int(product.price)
        data['currency'] = product.currency
        data['amount'] = price

        data['cart.items[0].name'] = product.title
        data['cart.items[0].merchantItemId'] = product.id
        data['cart.items[0].quantity'] = 1
        data['cart.items[0].price'] = price
        data['cart.items[0].originalPrice'] = price

    if user is not None:
        cards = CreditCard.objects.filter(user_id=user.get('id'))
        transaction_id = '{}/{}'.format(request.user.id, transaction_id)

        data['customer.givenName'] = user.get('first_name')
        data['customer.surname'] = user.get('surname_name')
        data['customer.mobile'] = user.get('phone_number')
        data['customer.email'] = user.get('email')

        profile = user.get('profile', None)
        if profile is not None:
            data['customer.companyName'] = profile.get('practice_name')



    data['merchantTransactionId'] = transaction_id
    for index, card in enumerate(cards):
        key = 'registrations[{}].id'.format(index)
        data[key] = card.registration_id

    return data

def save_card(user, registration_id, data):

    try:
        card = CreditCard.objects.get(registration_id=registration_id)
    except CreditCard.DoesNotExist:
        card = {
            'user_id': user.id,
            'registration_id': registration_id,
            'cardholder_name': data.get('holder'),
            'expiry_month': data.get('expiryMonth'),
            'expiry_year': data.get('expiryYear'),
            'last_four_digits': data.get('last4Digits'),
            'bin': data.get('bin'),
        }
        card = CreditCard.objects.create(**card)
    return card

def save_transaction(user, data):

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

    transaction = Transaction.objects.create(**transaction)
    if data.get('card', None) is not None and user is not None:
        card = save_card(user, data.get('registrationId'), data.get('card'))
        transaction.card = card
        transaction.save()

    return transaction

def repeat_payment():
    '''
    curl https://test.oppwa.com/v1/registrations/../payments \
    -d "authentication.userId=.." \
    -d "authentication.password=.." \
    -d "authentication.entityId=.." \
    -d "amount=92.00" \
    -d "currency=ZAR" \
    -d "paymentType=DB" \
    -d "recurringType=REPEATED"
    '''
    pass
