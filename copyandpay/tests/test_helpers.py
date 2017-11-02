from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from ..models import CreditCard
from ..helpers import prepare_checkout_data, \
    recurring_transaction_data_from_transaction,\
    send_receipt

from .utils import create_user, create_product, create_card, create_transaction
from .datas import SUCCESS_PAYMENT
import responses, unittest

def assert_fields(expected_fields, data):
    for field in expected_fields:
        assert data.get(field, None is not None)

class PrepareCheckoutDataTestCase(TestCase):

    def setUp(self):
        factory = RequestFactory()
        self.user = create_user()
        self.request = factory.get('/pay')
        self.request.user = self.user

    def test_minimum_requirements_with_non_logged_in_user(self):
        expected_fields = [
            'merchantTransactionId',
            'authentication.userId',
            "authentication.password",
            "authentication.entityId",
            "createRegistration",
            "paymentType"
        ]
        self.request.user = AnonymousUser()
        result = prepare_checkout_data(self.request)

        assert_fields(expected_fields, result)

    def test_minimum_requirements_with_logged_in_user(self):
        result = prepare_checkout_data(self.request)

    def test_post_data_is_added_to_request(self):
        pass

    @unittest.skip('todo: update test')
    def test_registered_cards_are_added_to_data(self):
        cc1 = create_card()
        cc2 = create_card()
        mock_user = {
            "id": self.user.id
        }
        result = prepare_checkout_data(self.request, mock_user)

        ids=[id.get('registration_id') for id in CreditCard.objects.all().values('registration_id')]
        assert result['registrations[0].id'] in ids
        assert result['registrations[1].id'] in ids


    def test_product_data_added_if_product_is_supplied(self):
        product = create_product()
        mock_user = {
            "id": self.user.id
        }
        result = prepare_checkout_data(self.request, mock_user, product)

        transaction_id_parts = result['merchantTransactionId'].split('/')

        assert int(transaction_id_parts[0]) == self.user.id,\
            'Expected {}. got: {}: {}'.format(transaction_id_parts[0], self.user.id, result['merchantTransactionId'])
        assert int(transaction_id_parts[1]) == product.id

class RecurringTransactionPayloadTestCase(TestCase):

    def setUp(self):
        self.transaction = create_transaction()

    def test_prepare_payload(self):
        recurring_transaction_data_from_transaction(SUCCESS_PAYMENT)

    @responses.activate
    def test_send_receipt(self):

        responses.add(
            responses.POST,
            'https://communicationguru.appointmentguru.co/communications/')

        send_receipt(self.transaction, self.transaction.customer)

