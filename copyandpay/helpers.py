from django.conf import settings
from django.template.loader import render_to_string
from .models import CreditCard, ScheduledPayment
from appointmentguru.communicationguru import CommunicationGuru
from slackclient import SlackClient
from dateutil.relativedelta import *
import requests, json, uuid, os, datetime

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
        cards = CreditCard.objects.filter(owner_id=user.get('id'))
        transaction_id = '{}/{}'.format(request.user.id, transaction_id)

        data['customer.merchantCustomerId'] = user.get('id')
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


def get_receipt_context(transaction):
    data = transaction.data
    # total = sum([float(item.get('price')) for item in data.get('cart',{}).get('items', [])])
    context = {
        'company': 'AppointmentGuru',
        'support_url': 'http://appointmentguru/help/',
        'transaction': transaction,
        'data': data,
        'total': transaction.price,
    }
    return context

def send_receipt(transaction, customer, subject=None):
    '''Send a receipt by email for the given transaction'''

    if subject is None:
        now = datetime.datetime.now()
        subject = 'Your receipt for {}'.format(now.strftime('%b %Y'))

    context = get_receipt_context(transaction)
    html = render_to_string('copyandpay/receipt.html', context)
    to_email = customer.email

    extra_data = {
        "owner": customer.owner_id,
        "object_ids": ["transaction:{}".format(transaction.id)]
    }

    return CommunicationGuru(settings.COMMUNICATIONGURU_URL)\
        .send_email(
            [to_email],
            subject,
            html,
            from_email=settings.DEFAULT_FROM_EMAIL,
            **extra_data)

def handle_transaction_result(transaction, scheduled_instance=None, reschedule=True, send_to_slack=True):
    '''Perform business logic based on the result of a transaction'''

    if transaction.status.startswith('success'):

        today = datetime.date.today()

        subject = '[AppointmentGuru] Your receipt for {}'.format(today.strftime('%b %Y'))

        send_receipt(transaction, transaction.customer, subject=subject)

        #re-schedule:
        next_month = today+relativedelta(months=+1)
        if reschedule:
            ScheduledPayment.from_transaction(transaction, next_month)
        if scheduled_instance is not None:
            scheduled_instance.status = 'success'
            scheduled_instance.save()

    if transaction.status.startswith('pending'):
        if scheduled_instance is not None:
            scheduled_instance.status = 'pending'
            scheduled_instance.save()

    if transaction.status.startswith('rejected'):

        if scheduled_instance is not None:
            scheduled_instance.status = 'failed'
            scheduled_instance.save()

    if send_to_slack:
        post_to_slack(json.loads(transaction.data))

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
