# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from copyandpay.models import Transaction
import responses, json

from .datas import SUCCESS_PAYMENT
from .utils import create_scheduled_payment

DATA = '''{"id": "8acda4a65dc5f75f015e0b0d35d3758c", "registrationId": "8acda4a25dc5f763015e0b0d34f4142a", "paymentType": "DB", "paymentBrand": "VISA", "amount": "200.00", "currency": "ZAR", "descriptor": "0847.3136.9170 AG01 Nedbank App", "merchantTransactionId": "None/1/30e317e8-a045-43c4-8893-37a73eed404d", "recurringType": "INITIAL", "result": {"code": "000.000.000", "description": "Transaction succeeded"}, "resultDetails": {"ExtendedDescription": "Approved", "ConnectorTxID2": "{CDAD95B8-F93A-4339-B5D5-797C840B5A5F}", "AcquirerResponse": "0", "ConnectorTxID1": "{D943BEFE-7B04-4B65-A476-E1E8408C0F31}", "clearingInstituteName": "NEDBANK"}, "card": {"bin": "479012", "binCountry": "ZA", "last4Digits": "1118", "holder": "R de Beer", "expiryMonth": "01", "expiryYear": "2018"}, "customer": {"givenName": "Taryn", "companyName": "Bananas and Burpees", "mobile": "+27765684520", "email": "bananas.burpees@gmail.com", "ip": "196.210.62.4"}, "customParameters": {"CTPE_DESCRIPTOR_TEMPLATE": ""}, "cart": {"items": [{"merchantItemId": "1", "name": "AppointmentGuru subscription (discounted)", "quantity": "1", "price": "200", "originalPrice": "200"}]}, "buildNumber": "6b1a3415e53ece34d6bb3f0421c774d82620c4ab@2017-08-10 11:34:40 +0000", "timestamp": "2017-08-22 17:46:10+0000", "ndc": "4F7AA9626EC1F26B5A777C22EF9CCEF5.prod01-vm-tx05"}'''

# class TransactionTestCase(TestCase):

#     def setUp(self):
#         transaction = Transaction()
#         transaction.registration_id = '123'
#         transaction.data = DATA

#         self.transaction = transaction

# class ScheduledPaymentTestCase(TestCase):

#     def setUp(self):
#         create_scheduled_payment(run_on_creation=True)

#     def test_it_hits_peach(self):
#         import ipdb;ipdb.set_trace()

#     def test_it_creates_a_transaction(self):
#         assert Transaction.objects.count() == 1