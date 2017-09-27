from django.core.management.base import BaseCommand, CommandError
from copyandpay.models import Transaction
class Command(BaseCommand):
    help = 'Make recurring payments'

    def handle(self, *args, **options):
        transactions = Transaction.objects.filter()

        for t in transactions:
            print (t)