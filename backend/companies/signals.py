from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Company
from subscriptions.models import Subscription

from .services import create_default_accounts

@receiver(post_save, sender=Company)
def create_company_subscription(sender, instance, created, **kwargs):
    if created:
        today = timezone.localdate()

        Subscription.objects.create(
            company=instance,
            status=Subscription.Status.TRIAL,
            trial_start=today,
            trial_end=today + timedelta(days=120),
        )
        
        create_default_accounts(instance)