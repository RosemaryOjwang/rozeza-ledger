from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from companies.models import Membership, Account


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