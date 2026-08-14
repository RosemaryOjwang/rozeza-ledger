from django.urls import path

from .views import (company_selection, select_company, company_workspace,)

urlpatterns = [
    path("companies/", company_selection, name="company_selection"),
    path("companies/<uuid:company_id>/select/", 
        select_company, name="select_company",
        ),
    path("workspace/", 
    company_workspace, 
    name="company_workspace"
    ),
]