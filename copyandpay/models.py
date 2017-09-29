# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.db import models

import requests, json, datetime, re

'''
    {u'amount': u'92.00',
     u'buildNumber': u'5afc05a9586b4307d3e0e7b9f8d131712d088597@2017-06-27 06:21:44 +0000',
     u'card': {u'bin': u'510510',
      u'expiryMonth': u'12',
      u'expiryYear': u'2017',
      u'holder': u'Jane Doe',
      u'last4Digits': u'5100'},
     u'currency': u'ZAR',
     u'customParameters': {u'CTPE_DESCRIPTOR_TEMPLATE': u''},
     u'customer': {u'ip': u'196.212.60.84', u'ipCountry': u'ZA'},
     u'descriptor': u'9421.3247.4530 AG01 Nedbank 3DS',
     u'id': u'8a82944a5ccfcf4c015cea66daf77583',
     u'ndc': u'9A43FEFC58248ED7FC22E0017CA0D352.sbg-vm-tx02',
     u'paymentBrand': u'MASTER',
     u'paymentType': u'DB',
     u'registrationId': u'8a82944a5ccfcf4c015cea66da437576',
     u'result': {u'code': u'000.100.110',
      u'description': u"Request successfully processed in 'Merchant in Integrator Test Mode'"},
     u'timestamp': u'2017-06-27 16:33:48+0000'}
'''

class CreditCard(models.Model):

    def __str__(self):
        return '{} ****{}'.format(self.cardholder_name, self.last_four_digits)

    owner_id = models.CharField(max_length=36)
    cardholder_name = models.CharField(max_length=255)
    registration_id = models.CharField(max_length=46)
    bin = models.CharField(max_length=255)
    expiry_month = models.PositiveIntegerField()
    expiry_year = models.PositiveIntegerField()
    last_four_digits = models.PositiveIntegerField()

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

RECURRANCE_RATES = [
    ('M', 'Monthly'),
    ('A', 'Annually'),
]

class Product(models.Model):

    def __str__(self):
        return self.title

    currency = models.CharField(max_length=6)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    is_recurring = models.BooleanField(default=False)
    recurrance_rate = models.CharField(max_length=22, default='M', choices=RECURRANCE_RATES)

class UserProduct(models.Model):
    user = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def charge(self):
        '''
        Create a charge on a recurring product
        '''
        pass

class Transaction(models.Model):

    def __str__(self):
        return '#{} - '.format(self.transaction_id, self.customer_name)

    user_product = models.ForeignKey(UserProduct, on_delete=models.SET_NULL, related_name='user_transaction', null=True, blank=True)
    card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, related_name='card_transaction', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_transaction', null=True, blank=True)

    initial_transaction = models.ForeignKey('Transaction', null=True, blank=True, on_delete=models.SET_NULL, default=None)

    currency = models.CharField(max_length=6)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    transaction_id = models.CharField(max_length=255)
    ndc = models.CharField(max_length=255, null=True, blank=True)
    payment_brand = models.CharField(max_length=255, null=True, blank=True)
    payment_type = models.CharField(max_length=6)
    registration_id = models.CharField(max_length=42, null=True, blank=True)

    result_code = models.CharField(max_length=22)
    result_description = models.TextField(null=True, blank=True)

    data = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return self.merged_data.get('customer',{}).get('givenName')

    @property
    def is_initial(self):
        '''Is this an original (e.g.: manual) payment?'''
        return self.initial_transaction is None

    @property
    def status(self):
        '''Based on peach payment result regexes, returns the status of this transaction'''

        regex_statuses = [
            # success \o/
            ('^(000\.000\.|000\.100\.1|000\.[36])', 'success'),
            ('^(000\.400\.0|000\.400\.100)', 'success_review_required'),
            # pending:
            ('^(000\.200)', 'pending'),
            ('^(800\.400\.5|100\.400\.500)', 'pending_long_term'),
            # rejections
            ('^(000\.400\.[1][0-9][1-9]|000\.400\.2)', 'rejected_3d_secure'),
            ('^(800\.[17]00|800\.800\.[123])', 'rejected_by_payment_system_or_bank'),
            ('^(900\.[1234]00)', 'rejected_communication_error'),
            ('^(800\.5|999\.|600\.1|800\.800\.8)', 'rejected_system_error'),
            ('^(100\.39[765])', 'rejected_async_workflow_error'),
            ('^(100\.400|100\.38|100\.370\.100|100\.370\.11)', 'rejected_risk'),
            ('^(800\.400\.1)', 'rejected_address_validation'),
            ('^(800\.400\.2|100\.380\.4|100\.390)', 'rejected_3d_secure'),
            ('^(100\.100\.701|800\.[32])', 'rejected_blacklist'),
            ('^(800\.1[123456]0)', 'rejected_risk_validation'),
            ('^(600\.[23]|500\.[12]|800\.121)', 'rejected_config_validation'),
            ('^(100\.[13]50)', 'rejected_registration_validation'),
            ('^(100\.250|100\.360)', 'rejected_job_validation'),
            ('^(700\.[1345][05]0)', 'rejected_reference_validation'),
            ('^(200\.[123]|100\.[53][07]|800\.900|100\.[69]00\.500)', 'rejected_format_validation'),
            ('^(100\.800)', 'rejected_address_validation'),
            ('^(100\.[97]00)', 'rejected_contact_validation'),
            ('^(100\.100|100.2[01])', 'rejected_account_validation'),
            ('^(100\.55)', 'rejected_amount_validation'),
            ('^(100\.380\.[23]|100\.380\.101)', 'rejected_risk_management'),
            ('^(000\.100\.2)', 'chargeback'),
        ]
        for regex, result in regex_statuses:
            if re.match(regex,self.result_code) is not None:
                return result

    @property
    def merged_data(self):
        '''
        format and merge data from this template and it's parent if necessary
        '''
        data = {}
        if self.initial_transaction is not None:
            data = json.loads(self.initial_transaction.data)

        data.update(json.loads(self.data))
        return data

    def make_recurring_payment(self):
        '''
from copyandpay.models import Transaction
t = Transaction.objects.first()
result = t.make_recurring_payment()
        '''
        from .helpers import recurring_transaction_data_from_transaction

        recurring_types = ['INITIAL', 'REPEATED']
        data = json.loads(self.data)

        base_url = settings.PEACH_BASE_URL
        payment_type = data.get('recurringType')
        registration_id = data.get('registrationId')

        if payment_type in recurring_types:
            url = '{}/v1/registrations/{}/payments'\
                .format(base_url, registration_id)

            payload = recurring_transaction_data_from_transaction(data)
            print(payload)
            result = requests.post(url, payload)
            if result.json().get('id', None) is not None:
                from .helpers import save_transaction
                transaction = save_transaction(None, result.json())
                transaction.initial_transaction_id = self.id
                transaction.save()
                return transaction
            else:
                return result
        else:
            print('Transaction is not a recurring type')

TRANSACTION_STATUSES = [
    ('new', 'new'),
    ('success', 'success'),
    ('failed', 'failed'),
    ('pending', 'pending'),
]

class ScheduledPayment(models.Model):
    '''A means to schedule payments'''

    transaction = models.ForeignKey('Transaction', null=True, blank=True, on_delete=models.SET_NULL, default=None)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=10, default='new', choices=TRANSACTION_STATUSES)

    def create_payment(self):
        '''Will attempt to make a payment hit based on the related transaction'''
        transaction = self.transaction.make_recurring_payment()

        # if transaction.is_successful:
        #     send_receipt
        # else:
        #     send_failure_message
        #     schedule_for_tomorrow

        # if transaction.card_expires_soon:
        #     send_card_expires_message

        return transaction


'''
curl https://test.oppwa.com/v1/registrations/{id}/payments \
	-d "authentication.userId=8a8294174e735d0c014e78cf266b1794" \
	-d "authentication.password=qyyfHCN83e" \
	-d "authentication.entityId=8a8294174e735d0c014e78cf26461790" \
	-d "amount=92.00" \
	-d "currency=ZAR" \
	-d "paymentType=PA" \
	-d "recurringType=REPEATED"
'''



