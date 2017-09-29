from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from ..models import CreditCard
from ..helpers import prepare_checkout_data, \
    save_card,\
    recurring_transaction_data_from_transaction,\
    send_receipt

from .utils import create_user, create_product, create_card, create_transaction
from .datas import SUCCESS_PAYMENT
import responses, unittest

def assert_fields(expected_fields, data):
    for field in expected_fields:
        assert data.get(field, None is not None)

class SaveCardTestCase(TestCase):

    def setUp(self):
        self.card_data = {
            'holder': 'Jane Doe',
            'expiryMonth': 10,
            'expiryYear': 17,
            'last4Digits': 1234,
            'bin': 111111,
        }
        self.registration_id = 1
        self.user = create_user()
        self.card = save_card(self.user, self.registration_id, self.card_data)

    def test_creates_card(self):
        card_count = CreditCard.objects.count()
        assert card_count == 1, \
            'Expected exactly 1 card. Got: {}'.format(card_count)

    def test_does_not_create_duplicate_cards_and_returns_existing_card(self):
        id = self.card.registration_id
        card = save_card(self.user, self.registration_id, self.card_data)

        assert self.card.id == card.id

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

        send_receipt(self.transaction)

