from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from ..helpers import prepare_checkout_data
from .utils import create_user, create_product, create_card

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

    def test_registered_cards_are_added_to_data(self):
        cc1 = create_card(self.user)
        cc2 = create_card(self.user)

        result = prepare_checkout_data(self.request)

        assert result['registrations[0].id'] == cc1.registration_id,\
            'Expected "registrations[0].id" to be: {}. Data: {}' .format(cc1.registration_id, result)
        assert result['registrations[1].id'] == cc2.registration_id

    def test_product_data_added_if_product_is_supplied(self):
        product = create_product()
        result = prepare_checkout_data(self.request, product)

        transaction_id_parts = result['merchantTransactionId'].split('/')
        assert int(transaction_id_parts[0]) == self.user.id,\
            'Expected {}. got: {}: {}'.format(transaction_id_parts[0], self.user.id, result['merchantTransactionId'])
        assert int(transaction_id_parts[1]) == product.id




