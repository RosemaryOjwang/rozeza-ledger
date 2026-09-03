# Rozeza Ledger — Database Design

## 1. Purpose

This document defines the database structure and accounting relationships for Rozeza Ledger.

The database must support accurate double-entry accounting, multiple companies, auditability, and automated financial reporting.

---

## 2. Core Accounting Principle

Every financial transaction recorded in Rozeza Ledger must follow the double-entry accounting principle.

Each transaction must have:

- At least one debit
- At least one credit
- Total debits equal to total credits

A journal entry cannot be posted if it does not balance.

---

## 3. Account Types

Rozeza Ledger will initially support five primary account types:

1. Assets
2. Liabilities
3. Equity
4. Revenue
5. Expenses

### Normal Balances

| Account Type | Normal Balance |
|--------------|----------------|
| Assets       | Debit          |
| Expenses     | Debit          |
| Liabilities  | Credit         |
| Equity       | Credit         |
| Revenue      | Credit         |

---

## 4. Chart of Accounts

Each company will have its own Chart of Accounts.

The Chart of Accounts will support:

- Account code
- Account name
- Account type
- Parent account
- Description
- Active/inactive status
- System/default account indicator

Example structure:

1000 — Assets
2000 — Liabilities
3000 — Equity
4000 — Revenue
5000 — Cost of Sales
6000 — Expenses

---

## 5. Initial Account Structure

### Assets

1000 Assets

1100 Current Assets

1110 Cash
1120 Petty Cash
1130 Bank
1140 Accounts Receivable
1150 Inventory

1200 Non-Current Assets

1210 Furniture
1220 Equipment
1230 Motor Vehicles

### Liabilities

2000 Liabilities

2100 Current Liabilities

2110 Accounts Payable
2120 Tax Payable

2200 Non-Current Liabilities

2210 Long-Term Loans

### Equity

3000 Equity

3100 Owner's Capital
3200 Retained Earnings

### Revenue

4000 Revenue

4100 Sales Revenue
4200 Service Revenue

### Cost of Sales

5000 Cost of Sales

5100 Cost of Goods Sold

### Expenses

6000 Expenses

6100 Rent Expense
6200 Electricity Expense
6300 Salaries Expense
6400 Transport Expense
6500 Communication Expense
6600 Other Operating Expenses

---

## 6. Journal Entries

A journal entry represents an accounting transaction.

Each journal entry contains one or more journal lines.

Example:

Customer purchases goods worth KSh 10,000 on credit.

Debit:
Accounts Receivable — KSh 10,000

Credit:
Sales Revenue — KSh 10,000

If inventory is involved:

Debit:
Cost of Goods Sold

Credit:
Inventory

The total debits must equal the total credits.

---

## 7. Transaction Automation

Rozeza Ledger should automatically generate accounting entries for common business transactions.

Examples:

### Customer Payment

Debit:
Bank/Cash

Credit:
Accounts Receivable

### Expense Payment

Debit:
Relevant Expense Account

Credit:
Bank/Cash

### Supplier Payment

Debit:
Accounts Payable

Credit:
Bank/Cash

### Owner Capital Contribution

Debit:
Bank/Cash

Credit:
Owner's Capital

---

## 8. Auditability

Financial transactions must maintain an audit trail.

The system should record:

- User who created the transaction
- Date and time
- Transaction reference
- Date of transaction
- Posting status
- Changes where applicable
- Reversal information

Posted accounting entries should not be silently altered.

Corrections should preferably be handled through reversal or correcting entries.

---

## 9. Opening Balances

Rozeza Ledger should support opening balances when an existing business starts using the system.

Opening balances must balance before they can be posted.

---

## 10. Future Considerations

The architecture should allow future support for:

- VAT and other taxes
- Inventory management
- Payroll
- Bank integrations
- Multi-currency
- Budgeting
- Advanced analytics
- AI-powered financial insights