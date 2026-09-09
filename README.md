# Rozeza Ledger

> A multi-company accounting and financial management platform for small and medium-sized businesses.

Rozeza Ledger is a web-based accounting system being developed to simplify financial management for businesses by bringing accounting, transactions, reporting, and business financial information into one platform.

The project is being developed with a focus on simplicity, automation, multi-company support, and extensibility.

---

## Project Status

**Current milestone: Multi-company foundation and initial dashboard completed.**

The core foundation of the application is now in place. Users can authenticate, belong to multiple companies, select an active company, switch between companies, and access a company-specific workspace.

The initial accounting dashboard interface has also been implemented.

---

## Demo

![Watch Rozeza Ledger Demo](demo/rozeza_ledger_demo.mp4)

---

## Core Features

### Authentication

- Custom Django user model
- User authentication
- Superuser support
- User-specific company memberships

### Multi-Company Management

A user can belong to multiple companies from a single Rozeza Ledger account.

Current functionality includes:

- Company registration
- Multiple companies per user
- Company memberships
- Company-specific roles
- Company selection
- Active company management
- Company switching
- Company-specific workspace

### Membership & Roles

The membership system currently supports:

- Owner
- Admin
- Accountant
- Staff

Each membership connects a user to a specific company and defines their role within that company.

### Company Workspace

Each selected company has its own workspace containing:

- Company information
- Current user role
- Dashboard
- Accounting navigation
- Business navigation
- Reports navigation
- Quick actions
- Company switching

### Initial Dashboard

The dashboard currently provides the visual foundation for the accounting system, including:

- Cash & Bank summary
- Receivables summary
- Payables summary
- Net Income summary
- Income vs Expenses section
- Recent Transactions section
- Quick Actions

Financial figures are currently placeholders and will be connected to the accounting engine as development progresses.

---

# Technology Stack

## Backend

- Python
- Django
- Django ORM
- Django Authentication
- PostgreSQL

## Frontend

The current interface uses:

- HTML
- CSS
- Django Templates

The frontend architecture may be expanded as the product develops.

## Database

- PostgreSQL

UUIDs are used for key entities such as companies and memberships to provide unique identifiers that are suitable for a multi-company application.

## Development Tools

- Git
- GitHub
- Visual Studio Code
- Python virtual environment

---

# System Architecture

The current application follows a Django-based architecture:

```text
Rozeza Ledger
│
├── Authentication
│       │
│       └── Custom User
│
├── Companies
│       │
│       ├── Company
│       └── Membership
│
├── Core
│       │
│       ├── Company Selection
│       ├── Company Switching
│       ├── Active Company Session
│       └── Company Workspace
│
└── Accounting
        │
        └── Being implemented

[def]: demo/rozeza_ledger_demo.mp4