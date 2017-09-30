# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CreditCard, Transaction, Product, UserProduct, ScheduledPayment

class ScheduledPaymentInline(admin.TabularInline):
    model = ScheduledPayment

class ProductAdmin(admin.ModelAdmin):
    """ServiceAdmin"""
    list_display = ('title', 'description', 'currency', 'price')

class UserProductAdmin(admin.ModelAdmin):
    """ServiceAdmin"""
    list_display = ('user', 'product',)

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'card', 'status', 'result_code', 'result_description', 'is_initial', 'currency', 'price')
    search_fields = ('transaction_id','registration_id',)
    # list_filter = ('status', 'result_code', 'is_initial',)
    inlines = [ScheduledPaymentInline]

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('bin', 'cardholder_name', 'expiry_month', 'expiry_year', 'last_four_digits')

class ScheduledPaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'scheduled_date', 'status')

admin.site.register(Product, ProductAdmin)
admin.site.register(UserProduct, UserProductAdmin)
admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(ScheduledPayment, ScheduledPaymentAdmin)


