from .models import Account

def create_default_accounts(company):
    """
    Create the default Chart of Accounts for a company.
    """

    accounts = [
        # Assets
        {
            "code": "1000",
            "name": "Assets",
            "account_type": Account.AccountType.ASSET,
            "is_system": True,
        },
        {
            "code": "1010",
            "name": "Cash",
            "account_type": Account.AccountType.ASSET,
            "parent_code": "1000",
            "is_system": True,
        },
        {
            "code": "1020",
            "name": "Bank",
            "account_type": Account.AccountType.ASSET,
            "parent_code": "1000",
            "is_system": True,
        },
        {
            "code": "1030",
            "name": "Accounts Receivable",
            "account_type": Account.AccountType.ASSET,
            "parent_code": "1000",
            "is_system": True,
        },
        {
            "code": "1040",
            "name": "Inventory",
            "account_type": Account.AccountType.ASSET,
            "parent_code": "1000",
            "is_system": True,
        },

        # Liabilities
        {
            "code": "2000",
            "name": "Liabilities",
            "account_type": Account.AccountType.LIABILITY,
            "is_system": True,
        },
        {
            "code": "2010",
            "name": "Accounts Payable",
            "account_type": Account.AccountType.LIABILITY,
            "parent_code": "2000",
            "is_system": True,
        },
        {
            "code": "2020",
            "name": "Loans Payable",
            "account_type": Account.AccountType.LIABILITY,
            "parent_code": "2000",
            "is_system": True,
        },
        {
            "code": "2030",
            "name": "Tax Payable",
            "account_type": Account.AccountType.LIABILITY,
            "parent_code": "2000",
            "is_system": True,
        },

        # Equity
        {
            "code": "3000",
            "name": "Equity",
            "account_type": Account.AccountType.EQUITY,
            "is_system": True,
        },
        {
            "code": "3010",
            "name": "Owner's Capital",
            "account_type": Account.AccountType.EQUITY,
            "parent_code": "3000",
            "is_system": True,
        },
        {
            "code": "3020",
            "name": "Owner's Drawings",
            "account_type": Account.AccountType.EQUITY,
            "parent_code": "3000",
            "is_system": True,
        },
        {
            "code": "3030",
            "name": "Retained Earnings",
            "account_type": Account.AccountType.EQUITY,
            "parent_code": "3000",
            "is_system": True,
        },

        # Revenue
        {
            "code": "4000",
            "name": "Revenue",
            "account_type": Account.AccountType.REVENUE,
            "is_system": True,
        },
        {
            "code": "4010",
            "name": "Sales Revenue",
            "account_type": Account.AccountType.REVENUE,
            "parent_code": "4000",
            "is_system": True,
        },
        {
            "code": "4020",
            "name": "Service Revenue",
            "account_type": Account.AccountType.REVENUE,
            "parent_code": "4000",
            "is_system": True,
        },
        {
            "code": "4030",
            "name": "Other Income",
            "account_type": Account.AccountType.REVENUE,
            "parent_code": "4000",
            "is_system": True,
        },

        # Expenses
        {
            "code": "5000",
            "name": "Expenses",
            "account_type": Account.AccountType.EXPENSE,
            "is_system": True,
        },
        {
            "code": "5010",
            "name": "Cost of Goods Sold",
            "account_type": Account.AccountType.EXPENSE,
            "parent_code": "5000",
            "is_system": True,
        },
        {
            "code": "5020",
            "name": "Salaries & Wages",
            "account_type": Account.AccountType.EXPENSE,
            "parent_code": "5000",
            "is_system": True,
        },
        {
            "code": "5030",
            "name": "Rent",
            "account_type": Account.AccountType.EXPENSE,
            "parent_code": "5000",
            "is_system": True,
        },
        {
            "code": "5040",
            "name": "Utilities",
            "account_type": Account.AccountType.EXPENSE,
            "parent_code": "5000",
            "is_system": True,
        },
        {
            "code": "5050",
            "name": "Transport",
            "account_type": Account.AccountType.EXPENSE,
            "parent_code": "5000",
            "is_system": True,
        },
        {
            "code": "5060",
            "name": "Bank Charges",
            "account_type": Account.AccountType.EXPENSE,
            "parent_code": "5000",
            "is_system": True,
        },
        {
            "code": "5070",
            "name": "Other Expenses",
            "account_type": Account.AccountType.EXPENSE,
            "parent_code": "5000",
            "is_system": True,
        },
    ]

    # First create all accounts
    # This ensures parent accounts exist before we assign them.
    for account_data in accounts:
        Account.objects.get_or_create(
            company=company,
            code=account_data["code"],
            defaults={
                "name": account_data["name"],
                "account_type": account_data["account_type"],
                "is_system": account_data.get("is_system", False),
            },
        )

    # Then assign parent accounts
    for account_data in accounts:
        parent_code = account_data.get("parent_code")

        if parent_code:
            child = Account.objects.get(
                company=company,
                code=account_data["code"],
            )

            parent = Account.objects.get(
                company=company,
                code=parent_code,
            )

            if child.parent_id != parent.id:
                child.parent = parent
                child.save(update_fields=["parent"])
