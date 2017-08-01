# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CreditCard, Transaction, Product, UserProduct

class ProductAdmin(admin.ModelAdmin):
    """ServiceAdmin"""
    list_display = ('title', 'description', 'currency', 'price')

class UserProductAdmin(admin.ModelAdmin):
    """ServiceAdmin"""
    list_display = ('user', 'product',)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'card', 'result_code', 'result_description', 'currency', 'price')

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('bin', 'cardholder_name', 'expiry_month', 'expiry_year', 'last_four_digits')

admin.site.register(Product, ProductAdmin)
admin.site.register(UserProduct, UserProductAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Transaction, TransactionAdmin)


