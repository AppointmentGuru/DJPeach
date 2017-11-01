from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ScheduledPayment

@receiver(post_save, sender=ScheduledPayment, dispatch_uid="copyandpay.signals.scheduled_payment_post_save")
def scheduled_payment_post_save(sender, instance, created, **kwargs):
    if created:
        # only send on creation (otherwise it will loop)
        if instance.run_on_creation:
            instance.run_recurring()
