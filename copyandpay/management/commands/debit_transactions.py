'''
Shell script to create scheduled and recurring payments
'''
from django.core.management.base import BaseCommand, CommandError
from copyandpay.models import ScheduledPayment
from copyandpay.helpers import post_to_slack, send_receipt, handle_transaction_result, post_to_slack
import datetime, json


class Command(BaseCommand):
    help = 'Make recurring payments'

    def handle(self, *args, **options):

        today = datetime.date.today()
        total_billed = 0
        today_formatted = today.strftime(today.strftime('%d %b %Y'))
        post_to_slack('Automated payments for: {}'.format(today_formatted))
        scheduled_transactions = ScheduledPayment.objects.filter(status='new', scheduled_date=today)
        for schedule in scheduled_transactions:
            result, transaction = schedule.run_recurring()
            total_billed = total_billed + float(transaction.price)

        # todo: take into account failed / pending
        post_to_slack('Total billed: {}'.format(total_billed))