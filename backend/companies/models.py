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

  
class Account(models.Model):
    class AccountType(models.TextChoices):
        ASSET = "ASSET", "Asset"
        LIABILITY = "LIABILITY", "Liability"
        EQUITY = "EQUITY", "Equity"
        REVENUE = "REVENUE", "Revenue"
        EXPENSE = "EXPENSE", "Expense"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="accounts",
    )

    code = models.CharField(
        max_length=20,
    )
    
    name = models.CharField(
        max_length=255,
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
    )

    description = models.TextField(
        blank=True,
    )

    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="sub_accounts",
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_system = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["code"]
        constraints = [
            models.UniqueConstraint(
                fields=["company", "code"],
                name="unique_account_code_per_company"
            ),
            models.UniqueConstraint(
                fields=["company", "name"],
                name="unique_account_name_per_company",
            ),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

class JournalEntry(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        POSTED = "POSTED", "Posted"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="journal_entries",
    )

    entry_date = models.DateField()

    reference = models.CharField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_journal_entries",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-entry_date", "-created_at"]

    def __str__(self):
        return f"{self.entry_date} - {self.description or 'Journal Entry'}"


class JournalEntryLine(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    journal_entry = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name="lines",
    )

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="journal_lines",
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    debit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    credit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.account} - Dr {self.debit} / Cr {self.credit}"

