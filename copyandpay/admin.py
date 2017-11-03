# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Customer, CreditCard, Transaction, Product, ScheduledPayment

class CustomerAdmin(admin.ModelAdmin):
    """CustomerAdmin"""
    list_display = ('owner_id', 'name', 'mobile', 'email', 'company')


class ProductAdmin(admin.ModelAdmin):
    """ServiceAdmin"""
    list_display = ('title', 'description', 'currency', 'price')

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'customer', 'transaction_id', 'card', 'status', 'result_code', 'result_description', 'currency', 'price')
    search_fields = ('transaction_id','registration_id',)
    # list_filter = ('status', 'result_code', 'is_initial',)
    # inlines = [ScheduledPaymentInline]

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('owner_id', 'bin', 'cardholder_name', 'expiry_month', 'expiry_year', 'last_four_digits')

class ScheduledPaymentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'card', 'amount', 'status', 'scheduled_date')

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ScheduledPayment, ScheduledPaymentAdmin)


