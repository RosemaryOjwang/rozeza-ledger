from datetime import timedelta
from django.utils import timezone

from .models import Subscription

def update_subscription_status(subscription):
    today = timezone.localdate

    if (
        subscription.status == Subscription.Status.Trial
        and  today > subscription.trial_end
    ):
        subscription.status = Subscription.Status.DEACTIVATED
        subscription.save(update_fields=["status", "updated_at"])

    return subscription

def activate_subscription_after_payment(subscription):
    today = timezone.localdate()

    subscription.status = Subscription.Status.ACTIVE
    subscription.subscription_start = today
    subscription.subscription_end = today + timezone.timedelta(days=365)

    subscription.save(
        update_fields=[
            "status",
            "subscription_start", 
            "subscription_end", 
            "updated_at",
            ]
        )
    return subscription

def renew_subscription(subscription):
    today = timezone.localdate()

    if (
        subscription.status == Subscription.Status.ACTIVE
        and subscription.subscription_end
        and subscription.subscription_end > today
    ):
        subscription.subscription_end = (
            subscription.subscription_end + timedelta(days=365)
        )

        subscription.save(
            update_fields=[
                "status",
                "subscription_end",
                "updated_at",
            ]
        )

    return subscription