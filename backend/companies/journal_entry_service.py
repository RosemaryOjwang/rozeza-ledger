
from decimal import Decimal, InvalidOperation
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from .models import AccountMapping, JournalEntry, JournalEntryLine


CENT = Decimal("0.01")
MAX_AMOUNT = Decimal("9999999999999.99")


def generate_journal_preview(
    company,
    transaction_type,
    selected_account_id,
    amount,
):
    """
    Generate a balanced two-line journal preview using
    the company's configured AccountMapping.

    This function does not save or post anything.
    """

    # 1. Validate transaction amount
    try:
        amount = Decimal(str(amount))
    except (InvalidOperation, TypeError, ValueError):
        raise ValidationError("Enter a valid transaction amount.")

    if not amount.is_finite():
        raise ValidationError("Transaction amount must be finite.")

    if amount <= 0:
        raise ValidationError(
            "Transaction amount must be greater than zero."
        )

    if amount > MAX_AMOUNT:
        raise ValidationError(
            "Transaction amount exceeds the allowed limit."
        )

    if amount != amount.quantize(CENT):
        raise ValidationError(
            "Transaction amount cannot have more than two decimal places."
        )

    amount = amount.quantize(CENT)

    # 2. Retrieve the company's active mapping
    mapping = (
        AccountMapping.objects
        .select_related(
            "selected_account",
            "counterpart_account",
        )
        .filter(
            company=company,
            transaction_type=transaction_type,
            selected_account_id=selected_account_id,
            is_active=True,
        )
        .first()
    )

    if not mapping:
        raise ValidationError(
            "No active account mapping exists for this transaction. "
            "Please configure the account mapping first."
        )

    selected_account = mapping.selected_account
    counterpart_account = mapping.counterpart_account

    # 3. Validate both accounts
    for account in (selected_account, counterpart_account):

        if account.company_id != company.id:
            raise ValidationError(
                "An account in the mapping belongs to another company."
            )

        if not account.is_active:
            raise ValidationError(
                f"{account.name} is inactive."
            )

        if account.sub_accounts.exists():
            raise ValidationError(
                f"{account.name} is a parent account. "
                "Select a posting-level account instead."
            )

    if selected_account.id == counterpart_account.id:
        raise ValidationError(
            "The selected and counterpart accounts cannot be the same."
        )

    # 4. Determine debit and credit sides
    if mapping.selected_account_side == AccountMapping.EntrySide.DEBIT:

        selected_debit = amount
        selected_credit = Decimal("0.00")

        counterpart_debit = Decimal("0.00")
        counterpart_credit = amount

    elif mapping.selected_account_side == AccountMapping.EntrySide.CREDIT:

        selected_debit = Decimal("0.00")
        selected_credit = amount

        counterpart_debit = amount
        counterpart_credit = Decimal("0.00")

    else:
        raise ValidationError(
            "Invalid account mapping entry side."
        )

    # 5. Generate journal lines
    lines = [
        {
            "account": selected_account,
            "debit": selected_debit,
            "credit": selected_credit,
        },
        {
            "account": counterpart_account,
            "debit": counterpart_debit,
            "credit": counterpart_credit,
        },
    ]

    # 6. Verify the generated entry
    total_debit = sum(
        (line["debit"] for line in lines),
        Decimal("0.00"),
    )

    total_credit = sum(
        (line["credit"] for line in lines),
        Decimal("0.00"),
    )

    if total_debit != total_credit:
        raise ValidationError(
            "Generated journal entry is not balanced."
        )

    return {
        "transaction_type": transaction_type,
        "amount": amount,
        "lines": lines,
        "total_debit": total_debit,
        "total_credit": total_credit,
        "is_balanced": True,
    }


def post_journal_entry(
    company,
    transaction_type,
    selected_account_id,
    amount,
    entry_date,
    created_by,
    submission_token,
    reference="",
    description="",
):
    """
    Rebuild and post a journal entry using the active account mapping.

    Saves the journal entry and its lines atomically.
    Repeated submissions with the same token return the existing entry.
    """

    # 1. Validate submission token
    try:
        submission_token = UUID(str(submission_token))
    except (TypeError, ValueError, AttributeError):
        raise ValidationError("Invalid journal submission token.")

    if not entry_date:
        raise ValidationError("Journal entry date is required.")

    if not created_by or not created_by.is_authenticated:
        raise ValidationError("An authenticated user is required.")

    # 2. Check whether this submission was already posted
    existing_entry = JournalEntry.objects.filter(
        submission_token=submission_token
    ).first()

    if existing_entry:
        if (
            existing_entry.company_id != company.id
            or existing_entry.created_by_id != created_by.id
        ):
            raise ValidationError(
                "This submission token belongs to another journal entry."
            )

        return existing_entry

    # 3. Recalculate the journal preview on the server
    preview = generate_journal_preview(
        company=company,
        transaction_type=transaction_type,
        selected_account_id=selected_account_id,
        amount=amount,
    )

    if not preview["is_balanced"]:
        raise ValidationError(
            "Cannot post an unbalanced journal entry."
        )

    # 4. Save the entry and lines atomically
    try:
        with transaction.atomic():

            journal_entry = JournalEntry.objects.create(
                company=company,
                transaction_type=transaction_type,
                entry_date=entry_date,
                reference=reference,
                description=description,
                status=JournalEntry.Status.POSTED,
                submission_token=submission_token,
                created_by=created_by,
            )

            journal_lines = [
                JournalEntryLine(
                    journal_entry=journal_entry,
                    account=line["account"],
                    debit=line["debit"],
                    credit=line["credit"],
                )
                for line in preview["lines"]
            ]

            JournalEntryLine.objects.bulk_create(journal_lines)

        return journal_entry

    except IntegrityError:
        # Another request may have posted the same token concurrently.
        existing_entry = JournalEntry.objects.filter(
            submission_token=submission_token
        ).first()

        if (
            existing_entry
            and existing_entry.company_id == company.id
            and existing_entry.created_by_id == created_by.id
        ):
            return existing_entry

        raise ValidationError(
            "The journal entry could not be posted. "
            "Please try again."
        )
