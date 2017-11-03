# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from copyandpay.models import Transaction
import responses, json

from .datas import SUCCESS_PAYMENT, RECURRING_SUCCESS
from .utils import create_scheduled_payment

from ..models import ScheduledPayment


DATA = '''{"id": "8acda4a65dc5f75f015e0b0d35d3758c", "registrationId": "8acda4a25dc5f763015e0b0d34f4142a", "paymentType": "DB", "paymentBrand": "VISA", "amount": "200.00", "currency": "ZAR", "descriptor": "0847.3136.9170 AG01 Nedbank App", "merchantTransactionId": "None/1/30e317e8-a045-43c4-8893-37a73eed404d", "recurringType": "INITIAL", "result": {"code": "000.000.000", "description": "Transaction succeeded"}, "resultDetails": {"ExtendedDescription": "Approved", "ConnectorTxID2": "{CDAD95B8-F93A-4339-B5D5-797C840B5A5F}", "AcquirerResponse": "0", "ConnectorTxID1": "{D943BEFE-7B04-4B65-A476-E1E8408C0F31}", "clearingInstituteName": "NEDBANK"}, "card": {"bin": "479012", "binCountry": "ZA", "last4Digits": "1118", "holder": "R de Beer", "expiryMonth": "01", "expiryYear": "2018"}, "customer": {"givenName": "Taryn", "companyName": "Bananas and Burpees", "mobile": "+27765684520", "email": "bananas.burpees@gmail.com", "ip": "196.210.62.4"}, "customParameters": {"CTPE_DESCRIPTOR_TEMPLATE": ""}, "cart": {"items": [{"merchantItemId": "1", "name": "AppointmentGuru subscription (discounted)", "quantity": "1", "price": "200", "originalPrice": "200"}]}, "buildNumber": "6b1a3415e53ece34d6bb3f0421c774d82620c4ab@2017-08-10 11:34:40 +0000", "timestamp": "2017-08-22 17:46:10+0000", "ndc": "4F7AA9626EC1F26B5A777C22EF9CCEF5.prod01-vm-tx05"}'''

# class TransactionTestCase(TestCase):

#     def setUp(self):
#         transaction = Transaction()
#         transaction.registration_id = '123'
#         transaction.data = DATA

#         self.transaction = transaction

class RecurringScheduledPaymentSuccessTestCase(TestCase):

    @responses.activate
    def setUp(self):
        reg_id = '1234'
        responses.add(
            responses.POST,
            'https://test.oppwa.com/v1/registrations/{}/payments'.format(reg_id),
            body=json.dumps(RECURRING_SUCCESS)
        )
        responses.add(
            responses.POST,
            'https://communicationguru.appointmentguru.co/communications/'
        )
        responses.add(
            responses.POST,
            'https://slack.com/api/chat.postMessage',
            body=json.dumps({}),
            status=201,
            content_type='application/json'
        )
        self.scheduled_payment = create_scheduled_payment(
            card_registration_id=reg_id,
            run_on_creation=True,
            is_recurring=True)
        self.reg_id = reg_id


    def test_it_hits_peach(self):
        '''This is verified in setup'''
        pass

    def test_it_creates_a_new_recurring_payment(self):
        new_scheduled_payment = ScheduledPayment.objects.last()
        assert new_scheduled_payment.id != self.scheduled_payment.id,\
            'New and old scheduled payment have the same id (no new shceduled payment was created! new:{} | old: {}'.format(new_scheduled_payment.id, self.scheduled_payment.id)

    def test_it_sets_status_to_new_for_new_scheduled_payment(self):
        new_scheduled_payment = ScheduledPayment.objects.last()
        assert new_scheduled_payment.status == 'new',\
            'Status should be new. Got: {}'.format(new_scheduled_payment.status)

    def test_it_sets_run_on_creation_false_for_new_scheduled_payment(self):
        new_scheduled_payment = ScheduledPayment.objects.last()
        assert new_scheduled_payment.run_on_creation == False,\
            'Status should be False. Got: {}'.format(new_scheduled_payment.run_on_creation)

    def test_it_sets_card_on_new_scheduled_payment(self):
        new_scheduled_payment = ScheduledPayment.objects.last()
        assert new_scheduled_payment.card.id == self.scheduled_payment.card.id

    def test_it_sets_product_on_new_scheduled_payment(self):
        new_scheduled_payment = ScheduledPayment.objects.last()
        assert new_scheduled_payment.product.id == self.scheduled_payment.product.id

    def test_it_sets_customer_on_new_scheduled_payment(self):
        new_scheduled_payment = ScheduledPayment.objects.last()
        assert new_scheduled_payment.customer.id == self.scheduled_payment.customer.id

    def test_it_creates_a_transaction(self):
        assert Transaction.objects.count() == 1

    def test_it_sets_transaction_customer(self):
        t = Transaction.objects.first()
        assert t.customer.id == self.scheduled_payment.customer.id

    def test_it_sets_transaction_card(self):
        t = Transaction.objects.first()
        assert t.card.id == self.scheduled_payment.card.id

    def test_it_sends_receipt(self):
        '''Verified in setup'''
        pass

    def test_it_posts_to_slack(self):
        '''Verified in setup'''
        pass