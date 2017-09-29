'''
Shell script to create scheduled and recurring payments
'''
from django.core.management.base import BaseCommand, CommandError
from copyandpay.models import ScheduledPayment
from copyandpay.helpers import post_to_slack, send_receipt, handle_transaction_result
import datetime, json


class Command(BaseCommand):
    help = 'Make recurring payments'

    def handle(self, *args, **options):

        today = datetime.date.today()
        scheduled_transactions = ScheduledPayment.objects.filter(status='new', scheduled_date=today)
        for schedule in scheduled_transactions:
            transaction = schedule.create_payment()

            handle_transaction_result(transaction, scheduled_instance=schedule)

