from django.urls import path


from .views import (
    company_selection, 
    select_company, 
    company_workspace, 
    chart_of_accounts, 
    add_account,
    journal_entries,
    add_journal_entry,
    journal_entry_detail,
    general_ledger,
    automated_journal_entry,
    account_mappings,
    )

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
    path(
    "journal-entries/",
    journal_entries,
    name="journal_entries",
    ),
    path(
    "journal-entries/add/",
    add_journal_entry,
    name="add_journal_entry",
    ),
    path(
    "journal-entries/<uuid:entry_id>/",
    journal_entry_detail,
    name="journal_entry_detail",
    ),
    path(
    "general-ledger/",
    general_ledger,
    name="general_ledger",
    ),
    path(
    "journal-entries/automated/",
    automated_journal_entry,
    name="automated_journal_entry",
    ),
    path(
    "account-mappings/",
    account_mappings,
    name="account_mappings",
    ),
]