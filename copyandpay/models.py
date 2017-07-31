# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings

from django.db import models

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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_cards')
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

    currency = models.CharField(max_length=6)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    is_recurring = models.BooleanField(default=False)
    recurrance_rate = models.CharField(max_length=22, default='M', choices=RECURRANCE_RATES)

class UserProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)

class Transaction(models.Model):

    user_product = models.ForeignKey(UserProduct, on_delete=models.SET_NULL, related_name='user_transaction', null=True, blank=True)
    card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, related_name='card_transaction', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='product_transaction', null=True, blank=True)

    currency = models.CharField(max_length=6)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    transaction_id = models.CharField(max_length=255)
    ndc = models.CharField(max_length=255)
    payment_brand = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=6)
    registration_id = models.CharField(max_length=42)

    result_code = models.CharField(max_length=22)
    result_description = models.TextField()

    data = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
