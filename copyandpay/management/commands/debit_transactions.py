from django.core.management.base import BaseCommand, CommandError
from copyandpay.models import Transaction
class Command(BaseCommand):
    help = 'Make recurring payments'

    def handle(self, *args, **options):
        transaction = Transaction.objects.get(id=args[0])
        transaction.make_recurring_payment()