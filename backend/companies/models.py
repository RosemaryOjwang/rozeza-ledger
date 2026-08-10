import uuid
from django.db import models
from django.conf import settings 

class Company(models.Model):
    """
    Represents a company in the rozeza system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,)
    name = models.CharField(max_length=255, unique=True,)
    legal_name = models.CharField(max_length=255, blank=True, null=True,)
    registration_number = models.CharField(max_length=100, blank=True,)
    kra_pin = models.CharField(max_length=20, blank=True,)
    email = models.EmailField(blank=True,)
    phone_number = models.CharField(max_length=20, blank=True,)
    country = models.CharField(max_length=100, default="Kenya",)
    currency = models.CharField(max_length=3, default="KES",)
    financial_year_start = models.DateField(null=True, blank=True,)
    is_active = models.BooleanField(default=True,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)

    class Meta:
        ordering = ["name"]
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER = "OWNER", "Owner"
        ADMIN = "ADMIN", "Admin"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        STAFF = "STAFF", "Staff"

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="memberships",
        )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="memberships",
        )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF,
        )
    is_active = models.BooleanField(default=True,)
    joined_at =models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "company"],
                name="unique_user_company_membership",
            )

        ]

    def __str__(self):
        return f"{self.user} - {self.company} ({self.get_role_display()})"

  