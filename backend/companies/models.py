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

class AccountMapping(models.Model):
    """
    Defines automatic counterpart account mappings
    for a company's transaction types.
    """

    class TransactionType(models.TextChoices):
        SALE = "SALE", "Sale"
        PURCHASE = "PURCHASE", "Purchase"
        EXPENSE = "EXPENSE", "Expense"
        CUSTOMER_RECEIPT = "CUSTOMER_RECEIPT", "Customer Receipt"
        SUPPLIER_PAYMENT = "SUPPLIER_PAYMENT", "Supplier Payment"
        BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
        LOAN_RECEIVED = "LOAN_RECEIVED", "Loan Received"
        LOAN_REPAYMENT = "LOAN_REPAYMENT", "Loan Repayment"
        CAPITAL_CONTRIBUTION = "CAPITAL_CONTRIBUTION", "Capital Contribution"

    class EntrySide(models.TextChoices):
        DEBIT = "DEBIT", "Debit"
        CREDIT = "CREDIT", "Credit"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="account_mappings",
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=TransactionType.choices,
    )

    selected_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="selected_mappings",
    )

    counterpart_account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name="counterpart_mappings",
    )

    selected_account_side = models.CharField(
        max_length=6,
        choices=EntrySide.choices,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "company",
                    "transaction_type",
                    "selected_account",
                ],
                name="unique_company_transaction_account_mapping",
            )
        ]

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.selected_account_id == self.counterpart_account_id:
            raise ValidationError(
                "Selected account and counterpart account "
                "cannot be the same."
            )

        if self.selected_account_id and self.company_id:
            if self.selected_account.company_id != self.company_id:
                raise ValidationError(
                    "Selected account must belong to this company."
                )

        if self.counterpart_account_id and self.company_id:
            if self.counterpart_account.company_id != self.company_id:
                raise ValidationError(
                    "Counterpart account must belong to this company."
                )

    def __str__(self):
        return (
            f"{self.company} - "
            f"{self.get_transaction_type_display()} - "
            f"{self.selected_account} -> "
            f"{self.counterpart_account}"
        )



class JournalEntry(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        POSTED = "POSTED", "Posted"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="journal_entries"
    )

    transaction_type = models.CharField(
        max_length=30,
        choices=AccountMapping.TransactionType.choices
    )

    entry_date = models.DateField()

    reference = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT
    )

    submission_token = models.UUIDField(
        null=True,
        blank=True,
        unique=True,
        editable=False
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_journal_entries"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-entry_date", "-created_at"]

    def __str__(self):
        return f"{self.company.name} - {self.entry_date} - {self.transaction_type}"


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

