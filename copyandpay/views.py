# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings

from .models import Transaction, Product
from .helpers import prepare_checkout_data, save_card, save_transaction, post_to_slack
from .appointmentguru import AppointmentGuru

import requests, uuid

def index(request):
    '''
    Purchase a product
    '''
    products = Product.objects.all()
    context = {
        "page_title": "Choose a product",
        "products": products
    }
    return render(request, 'copyandpay/products.html', context=context)


def payment_page(request, product_id):
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

    token = request.GET.get('t')
    guru = AppointmentGuru(token)
    me = guru.me()
    user_data = me.json().get('results')[0]

    product = Product.objects.get(id=product_id)
    data = prepare_checkout_data(request, user_data, product)

    url = '{}/v1/checkouts'.format(settings.PEACH_BASE_URL)
    response = requests.post(url, data)
    checkout_id = response.json().get('id')
    context = {
        'peach_base_url': settings.PEACH_BASE_URL,
        'result_url': settings.PEACH_RESULT_PAGE,
        'checkout_id': checkout_id,
        'me': user_data,
        'product': product,
    }
    return render(request, 'copyandpay/pay.html', context=context)

def result_page(request):

    base = settings.PEACH_BASE_URL
    path = request.GET.get('resourcePath')
    url = '{}{}'.format(base, path)
    payment_result = requests.get(url)
    payment_data = payment_result.json()
    # try:
    post_to_slack(payment_data)
    # except Exception:
    #     pass

    if payment_data.get('id', None) is not None:
        save_transaction(request.user, payment_result.json())
    else:
        # error
        pass


    context = {
        'result': payment_data
    }
    return render(request, 'copyandpay/result.html', context=context)


