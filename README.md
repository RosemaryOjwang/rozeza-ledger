# Rozeza Ledger

Rozeza Ledger is a modern cloud-based accounting and financial management platform built for small and medium-sized businesses in Kenya and across Africa.

The goal is to provide an intuitive, secure, and scalable accounting system that supports bookkeeping, financial reporting, invoicing, inventory management, and business analytics.

---

## Current Development Status

**Phase:** Foundation Complete

### Completed
- Django project setup
- PostgreSQL database configuration
- Custom User model
- Email-based authentication foundation
- Django Admin configuration
- Company model
- Multi-company foundation
- GitHub repository and project structure

### In Progress
- Membership model (Users ↔ Companies)
- Role-based access control
- Company onboarding workflow

---

## Technology Stack

### Backend
- Python 3.14
- Django 6.x
- Django REST Framework
- PostgreSQL

### Database
- PostgreSQL 18

### Development Tools
- Git
- GitHub
- VS Code

---

## Project Structure

backend/
├── accounts/          # Authentication & users
├── companies/         # Companies and company management
├── core/              # Shared utilities
└── config/            # Django settings

---

## Domain Models

### User
Custom authentication model using email-based login.

### Company
Represents a business using Rozeza Ledger.

Current fields include:
- UUID primary key
- Company name
- Legal name
- Registration number
- KRA PIN
- Email
- Phone number
- Country
- Currency
- Financial year start
- Active status
- Audit timestamps

---

## Development Roadmap

### Phase 1 – Foundation
- [x] Custom User
- [x] Company
- [ ] Membership
- [ ] Roles & Permissions
- [ ] Company Settings

### Phase 2 – Accounting Core
- [ ] Chart of Accounts
- [ ] Financial Periods
- [ ] Journal Entries
- [ ] General Ledger
- [ ] Trial Balance

### Phase 3 – Business Operations
- [ ] Customers
- [ ] Suppliers
- [ ] Products & Services
- [ ] Invoicing
- [ ] Payments

### Phase 4 – Reporting
- [ ] Profit & Loss
- [ ] Balance Sheet
- [ ] Cash Flow
- [ ] Tax Reports
- [ ] Dashboard & Analytics

---

## Team

### Rosemary Ojwang & Charles
## Team Development Tasks

### Current Sprint
- [x] Initialize Git repository
- [x] Configure Django project
- [x] Configure PostgreSQL
- [x] Implement custom User model
- [x] Build Company model
- [x] Register Company in Django Admin
- [ ] Implement Membership model
- [ ] Implement Role model
- [ ] Company onboarding flow
- [ ] Chart of Accounts
- [ ] Financial Periods
- [ ] Journal Entries
- [ ] General Ledger
- [ ] Trial Balance
- [ ] Financial Statements

### Zephaniah
**Head of Finance & Accounting Expert**
- Accounting rules
- Financial reporting validation
- Chart of accounts design
- Tax and compliance guidance

---

## Development Workflow

- Create a feature branch for every new feature.
- Commit changes in small, meaningful increments.
- Push branches to GitHub.
- Open a Pull Request for review before merging into main.

---

## Long-Term Vision

Rozeza Ledger is being designed as a multi-tenant SaaS platform where:

- One installation serves many companies.
- Users can belong to multiple companies.
- Each company's data remains completely isolated.
- Role-based permissions control access to financial information.

This architecture provides a strong foundation for future cloud deployment and commercial scaling.

---

## Project Status

**Foundation Completed Successfully**

The project now has a working PostgreSQL database, custom authentication, Django Admin access, and operational company management functionality. The next major milestone is implementing the Membership model to connect users and companies.