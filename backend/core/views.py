from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from companies.models import Membership


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