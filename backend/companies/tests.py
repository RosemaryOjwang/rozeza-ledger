
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Company, Account, AccountMapping
from .journal_entry_service import generate_journal_preview


class JournalPreviewServiceTests(TestCase):

    def setUp(self):
        """
        Create a test company and reuse the default accounts
        automatically generated for that company.
        """
        self.company = Company.objects.create(
            name="Test Company",
            currency="KES",
        )

        self.cash_account = Account.objects.get(
            company=self.company,
            code="1010",
        )

        self.sales_account = Account.objects.get(
            company=self.company,
            code="4010",
        )

        self.mapping = AccountMapping.objects.create(
            company=self.company,
            transaction_type=AccountMapping.TransactionType.SALE,
            selected_account=self.cash_account,
            counterpart_account=self.sales_account,
            selected_account_side=AccountMapping.EntrySide.DEBIT,
        )

    def test_generates_debit_and_credit_correctly(self):
        """A sale should generate equal debit and credit entries."""

        preview = generate_journal_preview(
            company=self.company,
            transaction_type=AccountMapping.TransactionType.SALE,
            selected_account_id=self.cash_account.id,
            amount="15000.00",
        )

        self.assertEqual(preview["amount"], Decimal("15000.00"))
        self.assertEqual(preview["total_debit"], Decimal("15000.00"))
        self.assertEqual(preview["total_credit"], Decimal("15000.00"))
        self.assertTrue(preview["is_balanced"])

        self.assertEqual(len(preview["lines"]), 2)

        self.assertEqual(
            preview["lines"][0]["account"],
            self.cash_account,
        )
        self.assertEqual(
            preview["lines"][0]["debit"],
            Decimal("15000.00"),
        )
        self.assertEqual(
            preview["lines"][0]["credit"],
            Decimal("0.00"),
        )

        self.assertEqual(
            preview["lines"][1]["account"],
            self.sales_account,
        )
        self.assertEqual(
            preview["lines"][1]["debit"],
            Decimal("0.00"),
        )
        self.assertEqual(
            preview["lines"][1]["credit"],
            Decimal("15000.00"),
        )

    def test_generates_credit_when_selected_account_side_is_credit(self):
        """The service should reverse debit and credit when configured."""

        self.mapping.selected_account_side = (
            AccountMapping.EntrySide.CREDIT
        )
        self.mapping.save()

        preview = generate_journal_preview(
            company=self.company,
            transaction_type=AccountMapping.TransactionType.SALE,
            selected_account_id=self.cash_account.id,
            amount="5000.00",
        )

        self.assertEqual(
            preview["lines"][0]["debit"],
            Decimal("0.00"),
        )
        self.assertEqual(
            preview["lines"][0]["credit"],
            Decimal("5000.00"),
        )

        self.assertEqual(
            preview["lines"][1]["debit"],
            Decimal("5000.00"),
        )
        self.assertEqual(
            preview["lines"][1]["credit"],
            Decimal("0.00"),
        )

        self.assertTrue(preview["is_balanced"])

    def test_rejects_missing_mapping(self):
        """The service should reject transactions without a mapping."""

        self.mapping.is_active = False
        self.mapping.save()

        with self.assertRaises(ValidationError):
            generate_journal_preview(
                company=self.company,
                transaction_type=AccountMapping.TransactionType.SALE,
                selected_account_id=self.cash_account.id,
                amount="1000.00",
            )

    def test_rejects_inactive_account(self):
        """The service should reject inactive accounts."""

        self.cash_account.is_active = False
        self.cash_account.save()

        with self.assertRaises(ValidationError):
            generate_journal_preview(
                company=self.company,
                transaction_type=AccountMapping.TransactionType.SALE,
                selected_account_id=self.cash_account.id,
                amount="1000.00",
            )

    def test_rejects_zero_amount(self):
        """Zero-value transactions should not be accepted."""

        with self.assertRaises(ValidationError):
            generate_journal_preview(
                company=self.company,
                transaction_type=AccountMapping.TransactionType.SALE,
                selected_account_id=self.cash_account.id,
                amount="0.00",
            )

    def test_rejects_negative_amount(self):
        """Negative transaction amounts should not be accepted."""

        with self.assertRaises(ValidationError):
            generate_journal_preview(
                company=self.company,
                transaction_type=AccountMapping.TransactionType.SALE,
                selected_account_id=self.cash_account.id,
                amount="-500.00",
            )

    def test_rejects_amount_with_more_than_two_decimal_places(self):
        """Amounts with more than two decimal places should be rejected."""

        with self.assertRaises(ValidationError):
            generate_journal_preview(
                company=self.company,
                transaction_type=AccountMapping.TransactionType.SALE,
                selected_account_id=self.cash_account.id,
                amount="1000.123",
            )
