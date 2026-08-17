from django.db import models

class Subscription(models.Model):

    class Status(models.TextChoices):
        TRIAL = "TRIAL", "Trial"
        ACTIVE = "ACTIVE", "Active"
        DEACTIVATED = "DEACTIVATED", "Deactivated"

    company = models.OneToOneField(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="subscription",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TRIAL,
    )

    trial_start = models.DateField()
    trial_end = models.DateField()

    subscription_start = models.DateField(
        null=True,
        blank=True,
    )

    subscription_end = models.DateField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.name} - {self.get_status_display()}"