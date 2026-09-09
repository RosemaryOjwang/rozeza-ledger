from django.urls import path


from .views import (company_selection, select_company, company_workspace, chart_of_accounts, add_account)

urlpatterns = [
    path("companies/", company_selection, name="company_selection"),
    path("companies/<uuid:company_id>/select/", 
        select_company, name="select_company",
        ),
    path("workspace/", 
    company_workspace, 
    name="company_workspace"
    ),
    path(
    "workspace/chart-of-accounts/",
    chart_of_accounts,
    name="chart_of_accounts",
    ),
    path(
    "chart-of-accounts/add/",
    add_account,
    name="add_account",
    ),
]