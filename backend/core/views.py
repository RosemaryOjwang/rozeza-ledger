from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.db import transaction

from companies.models import Membership, Account, JournalEntry


@login_required
def company_selection(request):
    memberships = (
        Membership.objects
        .filter(user=request.user, is_active=True)
        .select_related("company")
    )

    return render(
        request,
        "core/company_selection.html",
        {"memberships": memberships},
    )
@login_required
def select_company(request, company_id):
    membership = get_object_or_404(
        Membership,
        user=request.user,
        company_id=company_id,
        is_active=True,
    )

    request.session["active_company_id"] = str(membership.company_id)

    return redirect("company_workspace")  # Redirect to the company workspace or dashboard after selection

@login_required
def company_workspace(request):
    company_id = request.session.get("active_company_id")
    
    if not company_id:
        return redirect("company_selection")

    membership = get_object_or_404(
        Membership,
        user=request.user,
        company_id=company_id,
        is_active=True,
    )

    return render(
        request,
        "core/company_workspace.html",
        {"membership": membership,
        "company": membership.company,},
    )
    
@login_required
def chart_of_accounts(request):
    company_id = request.session.get("active_company_id")

    if not company_id:
        return redirect("company_selection")

    membership = get_object_or_404(
        Membership,
        user=request.user,
        company_id=company_id,
        is_active=True,
    )

    accounts = (
        Account.objects
        .filter(company=membership.company)
        .select_related("parent")
        .order_by("code")
    )

    return render(
        request,
        "core/chart_of_accounts.html",
        {
            "membership": membership,
            "company": membership.company,
            "accounts": accounts,
        },
    )    
    
@login_required
def add_account(request):
    company_id = request.session.get("active_company_id")

    if not company_id:
        return redirect("company_selection")

    membership = get_object_or_404(
        Membership,
        user=request.user,
        company_id=company_id,
        is_active=True,
    )

    company = membership.company

    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        name = request.POST.get("name", "").strip()
        account_type = request.POST.get("account_type")
        parent_id = request.POST.get("parent")

        if not code or not name or not account_type:
            messages.error(
                request,
                "Code, account name and account type are required."
            )

        elif Account.objects.filter(
            company=company,
            code=code
        ).exists():
            messages.error(
                request,
                "An account with this code already exists."
            )

        else:
            parent = None

            if parent_id:
                parent = get_object_or_404(
                    Account,
                    id=parent_id,
                    company=company,
                )

            Account.objects.create(
                company=company,
                code=code,
                name=name,
                account_type=account_type,
                parent=parent,
                is_system=False,
            )

            messages.success(
                request,
                "Account created successfully."
            )

            return redirect("chart_of_accounts")

    parent_accounts = (
        Account.objects
        .filter(
            company=company,
            parent__isnull=True,
        )
        .order_by("code")
    )

    account_types = Account.AccountType.choices

    return render(
        request,
        "core/add_account.html",
        {
            "membership": membership,
            "company": company,
            "parent_accounts": parent_accounts,
            "account_types": account_types,
        },
    )    

@login_required
def journal_entries(request):
    company_id = request.session.get("active_company_id")

    if not company_id:
        return redirect("company_selection")

    membership = get_object_or_404(
        Membership,
        user=request.user,
        company_id=company_id,
        is_active=True,
    )

    entries = (
        JournalEntry.objects
        .filter(company=membership.company)
        .prefetch_related("lines__account")
        .order_by("-entry_date", "-created_at")
    )

    return render(
        request,
        "core/journal_entries.html",
        {
            "membership": membership,
            "company": membership.company,
            "entries": entries,
        },
    )
    
@login_required
def add_journal_entry(request):
    company_id = request.session.get("active_company_id")

    if not company_id:
        return redirect("company_selection")

    membership = get_object_or_404(
        Membership,
        user=request.user,
        company_id=company_id,
        is_active=True,
    )

    company = membership.company

    accounts = (
        Account.objects
        .filter(
            company=company,
            is_active=True,
        )
        .order_by("code")
    )

    if request.method == "POST":
        entry_date = request.POST.get("entry_date")
        reference = request.POST.get("reference", "").strip()
        description = request.POST.get("description", "").strip()

        account_ids = request.POST.getlist("account")
        debits = request.POST.getlist("debit")
        credits = request.POST.getlist("credit")

        if not entry_date:
            messages.error(request, "Entry date is required.")

        elif not description:
            messages.error(request, "Description is required.")

        elif not account_ids:
            messages.error(request, "At least two journal lines are required.")

        else:
            lines = []
            total_debit = Decimal("0.00")
            total_credit = Decimal("0.00")
            has_error = False

            for account_id, debit, credit in zip(
                account_ids,
                debits,
                credits,
            ):
                if not account_id:
                    continue

                try:
                    account = Account.objects.get(
                        id=account_id,
                        company=company,
                        is_active=True,
                    )
                except Account.DoesNotExist:
                    messages.error(request, "Invalid account selected.")
                    has_error = True
                    break

                try:
                    debit_amount = Decimal(debit or "0")
                    credit_amount = Decimal(credit or "0")
                except InvalidOperation:
                    messages.error(
                        request,
                        "Debit and credit amounts must be valid numbers.",
                    )
                    has_error = True
                    break

                if debit_amount < 0 or credit_amount < 0:
                    messages.error(
                        request,
                        "Debit and credit amounts cannot be negative.",
                    )
                    has_error = True
                    break

                if debit_amount > 0 and credit_amount > 0:
                    messages.error(
                        request,
                        "A journal line cannot have both a debit and a credit.",
                    )
                    has_error = True
                    break

                if debit_amount == 0 and credit_amount == 0:
                    messages.error(
                        request,
                        "Each journal line must have a debit or credit amount.",
                    )
                    has_error = True
                    break

                total_debit += debit_amount
                total_credit += credit_amount

                lines.append(
                    {
                        "account": account,
                        "debit": debit_amount,
                        "credit": credit_amount,
                    }
                )

            if not has_error and len(lines) < 2:
                messages.error(
                    request,
                    "A journal entry must have at least two lines.",
                )
                has_error = True

            if not has_error and total_debit != total_credit:
                messages.error(
                    request,
                    f"Journal entry is not balanced. "
                    f"Debit: {total_debit:,.2f}, "
                    f"Credit: {total_credit:,.2f}.",
                )
                has_error = True

            if not has_error:
                with transaction.atomic():
                    journal_entry = JournalEntry.objects.create(
                        company=company,
                        entry_date=entry_date,
                        reference=reference,
                        description=description,
                        status=JournalEntry.Status.POSTED,
                        created_by=request.user,
                    )

                    for line in lines:
                        journal_entry.lines.create(
                            account=line["account"],
                            debit=line["debit"],
                            credit=line["credit"],
                        )

                messages.success(
                    request,
                    "Journal entry created successfully.",
                )

                return redirect("journal_entries")

    return render(
        request,
        "core/add_journal_entry.html",
        {
            "membership": membership,
            "company": company,
            "accounts": accounts,
        },
    )