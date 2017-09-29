# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import CreditCard, Transaction
from .utils import create_product

import responses, json, unittest

global_data = {
    u'amount': u'92.00',
    u'buildNumber': u'5afc05a9586b4307d3e0e7b9f8d131712d088597@2017-06-27 06:21:44 +0000',
    u'card': {
        u'bin': u'510510',
        u'expiryMonth': u'12',
        u'expiryYear': u'2017',
        u'holder': u'Jane Doe',
        u'last4Digits': u'5100'
    },
    u'customer': {
        'merchantItemId': '1',
		u'givenName': u'Joe',
		u'companyName': u'AppointmentGuru',
		u'mobile': u'+27832566533',
		u'email': u'tech@appointmentguru.co',
		u'ip': u'1.2.3.4'
	},
    u'currency': u'ZAR',
    u'customParameters': {u'CTPE_DESCRIPTOR_TEMPLATE': u''},
    u'customer': {u'ip': u'196.212.60.84', u'ipCountry': u'ZA'},
    u'descriptor': u'9421.3247.4530 AG01 Nedbank 3DS',
    u'id': u'8a82944a5ccfcf4c015cea66daf77583',
    u'ndc': u'9A43FEFC58248ED7FC22E0017CA0D352.sbg-vm-tx02',
    u'paymentBrand': u'MASTER',
    u'paymentType': u'DB',
    u'registrationId': u'8a82944a5ccfcf4c015cea66da437576',
    u'result': {
        u'code': u'000.100.110',
        u'description': u"Request successfully processed in 'Merchant in Integrator Test Mode'"
    },
    u'timestamp': u'2017-06-27 16:33:48+0000'
}

error_response_result_data = {
    u'buildNumber': u'5afc05a9586b4307d3e0e7b9f8d131712d088597@2017-06-27 06:21:44 +0000',
    u'timestamp': u'2017-06-27 21:08:29+0000',
    u'ndc': u'9a06a79a76264b73a3a25b823a808ada',
    u'result': {
        u'code': u'200.300.404',
        u'description': u'invalid or missing parameter - (opp) No payment session found for the requested id - are you mixing test/live servers or have you paid more than 30min ago?'
    }
}

class PaymentPageTestCase(TestCase):

    @responses.activate
    def setUp(self):

        responses.add(
            responses.POST,
            'https://test.oppwa.com/v1/checkouts',
            body=json.dumps({'id': '123'}),
        )

        self.user = get_user_model().objects.create_user('joe', 'joe@soap.com', 'pass')
        client = Client()
        login_result = client.login(username='joe', password='pass')
        self.product = create_product()
        self.url = reverse('payment_page', args=(self.product.id,))
        self.result = client.get(self.url)

    def test_is_ok(self):
        assert self.result.status_code == 200

    def test_adds_any_registration_ids_that_exist_to_payload(self):
        pass

class LoggedInUserPaymentTestCase(TestCase):

    @responses.activate
    def setUp(self):
        self.url = reverse('result_page')
        self.user = get_user_model().objects.create_user('joe', 'joe@soap.com', 'pass')
        login_result = self.client.login(username='joe', password='pass')

    def test_adds_any_registration_ids_that_exist(self):
        pass

class PaymentResultErrorTestCase(TestCase):

    @responses.activate
    def setUp(self):
        self.url = reverse('result_page')
        self.user = get_user_model().objects.create_user('joe', 'joe@soap.com', 'pass')
        client = Client()
        login_result = client.login(username='joe', password='pass')

        responses.add(
            responses.GET,
            'https://test.oppwa.com/v1/checkouts/123/payment',
            body=json.dumps(error_response_result_data),
            status=200,
            content_type='application/json'
        )

        responses.add(
            responses.POST,
            'https://slack.com/api/chat.postMessage',
            body=json.dumps({}),
            status=201,
            content_type='application/json'
        )

        data = {
            'resourcePath': '/v1/checkouts/123/payment'
        }
        self.result = client.get(self.url, data)

    def test_is_ok(self):
        assert self.result.status_code == 200

    def test_does_not_create_transaction(self):
        assert Transaction.objects.count() == 0

class PaymentResultReceivedTestCase(TestCase):

    @responses.activate
    def setUp(self):
        self.url = reverse('result_page')
        self.user = get_user_model().objects.create_user('joe', 'joe@soap.com', 'pass')
        login_result = self.client.login(username='joe', password='pass')
        data = {
            'resourcePath': '/v1/checkouts/123/payment'
        }

        responses.add(
            responses.GET,
            'https://test.oppwa.com/v1/checkouts/123/payment',
            body=json.dumps(global_data),
            status=200,
            content_type='application/json'
        )
        responses.add(
            responses.POST,
            'https://slack.com/api/chat.postMessage',
            body=json.dumps({}),
            status=201,
            content_type='application/json'
        )
        responses.add(
            responses.POST,
            'https://communicationguru.appointmentguru.co/communications/')


        self.result = self.client.get(self.url, data)

    def test_is_ok(self):
        assert self.result.status_code == 200

    def test_creates_transaction(self):
        assert Transaction.objects.count() == 1

    @unittest.skip("Needs an update")
    def test_creates_credit_card(self):
        assert CreditCard.objects.count() == 1



