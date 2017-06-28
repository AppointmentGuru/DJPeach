# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings

from .models import CreditCard, Transaction, Product
from .helpers import prepare_checkout_data, save_card, save_transaction

import requests, json, uuid

def product_purchase(request, product_id):
    '''
    Purchase a product
    '''
    pass


def payment_page(request):
    '''
    Once off payment

    curl https://test.oppwa.com/v1/checkouts \
    -d "authentication.userId=.." \
    -d "authentication.password=.." \
    -d "authentication.entityId=.." \
    -d "amount=92.00" \
    -d "currency=ZAR" \
    -d "paymentType=DB"
    '''
    product = Product.objects.first()
    data = prepare_checkout_data(request, product)

    url = 'https://test.oppwa.com/v1/checkouts'
    response = requests.post(url, data)
    checkout_id = response.json().get('id')
    context = {
        'checkout_id': checkout_id
    }
    return render(request, 'copyandpay/pay.html', context=context)

def result_page(request):

    base = settings.PEACH_BASE_URL
    path = request.GET.get('resourcePath')
    url = '{}{}'.format(base, path)
    payment_result = requests.get(url)

    if payment_result.json().get('id', None) is not None:
        save_transaction(request.user, payment_result.json())
    else:
        # error
        pass

    context = {'result': payment_result.json()}
    return render(request, 'copyandpay/result.html', context=context)


