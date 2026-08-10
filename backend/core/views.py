from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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