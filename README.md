# Product Requirements Document (PRD)

# Rozeza Ledger

**Version:** 1.0 (MVP)

**Status:** Draft

**Last Updated:** 7th August 2026

---

# 1. Executive Summary

Rozeza Ledger is a cloud-based accounting and business automation platform built to simplify financial management for Small and Medium-sized Enterprises (SMEs).

The platform combines modern cloud technologies with sound accounting principles to provide businesses with accurate financial records, automated bookkeeping workflows, and actionable business insights.

Rozeza Ledger is the flagship product under the **Rozeza** brand and serves as the foundation for a future suite of integrated business management applications.

---

# 2. Product Vision

To become Africa's leading intelligent accounting and business management platform, empowering businesses through simplicity, automation, and data-driven decision-making.

---

# 3. Mission Statement

Our mission is to simplify accounting for businesses by providing a secure, affordable, and intelligent platform that automates financial processes while delivering accurate reporting and meaningful business insights.

---

# 4. Problem Statement

Many SMEs continue to experience challenges managing their finances due to:

- Manual bookkeeping
- Spreadsheet-based accounting
- Delayed financial reporting
- Limited visibility into business performance
- Expensive accounting software
- Complex user interfaces
- Poor integration between business operations and accounting

These challenges reduce efficiency and make it difficult for business owners to make informed financial decisions.

Rozeza Ledger aims to solve these problems through intelligent automation and an intuitive user experience.

---

# 5. Product Objectives

The MVP aims to:

- Provide a complete cloud-based accounting platform for SMEs.
- Automate core accounting workflows.
- Generate accurate financial reports.
- Reduce manual bookkeeping.
- Improve financial visibility.
- Build a scalable technical foundation for future products.

---

# 6. Target Market

## Primary Customers

- Small Businesses
- Medium-sized Businesses
- Startups
- Schools
- Retail Shops
- Service Businesses
- NGOs
- Professional Firms

## Secondary Users

- Accountants
- Bookkeepers
- Auditors
- Financial Consultants

---

# 7. Business Goals

## Short-Term Goals (MVP)

- Complete MVP within three months.
- Validate product-market fit.
- Conduct pilot testing with selected businesses.
- Collect user feedback.

## Medium-Term Goals

- Acquire first paying customers.
- Build customer support processes.
- Launch Version 1.0.

## Long-Term Goals

Develop the Rozeza ecosystem including:

- Rozeza Ledger
- Rozeza Payroll
- Rozeza Inventory
- Rozeza CRM
- Rozeza HR
- Rozeza Analytics

---

# 8. Guiding Principles

Every feature added to Rozeza Ledger should satisfy at least one of the following:

- Reduce manual work
- Improve accounting accuracy
- Save users time
- Improve decision-making
- Maintain compliance
- Provide excellent user experience
- Scale with business growth

---

# 9. User Roles

## System Administrator

Responsibilities:

- Manage users
- Configure system settings
- Manage permissions
- View system logs

---

## Business Owner

Responsibilities:

- View dashboards
- Manage business operations
- Review reports
- Approve transactions

---

## Accountant

Responsibilities:

- Maintain Chart of Accounts
- Record journal entries
- Generate reports
- Perform reconciliations

---

## Cashier

Responsibilities:

- Receive payments
- Issue receipts
- Create invoices

---

## Auditor (Future)

Responsibilities:

- Read-only access
- Audit reports
- Audit trail review

---

# 10. MVP Functional Requirements

## Authentication

- User Registration
- Secure Login
- Password Reset
- Role-Based Access Control

---

## Company Management

- Company Profile
- Financial Year
- Company Settings
- Multiple Companies (Future Ready)

---

## Chart of Accounts

Users should be able to:

- Create accounts
- Edit accounts
- Archive accounts
- Categorize accounts
- Search accounts

---

## Journal Entries

Users should be able to:

- Create journal entries
- Edit draft entries
- Post journal entries
- Reverse entries
- View posting history

---

## General Ledger

- Account balances
- Transaction history
- Running balances
- Filtering

---

## Trial Balance

Generate Trial Balance by:

- Date
- Financial Period
- Financial Year

---

## Customer Management

- Create customers
- Edit customer profiles
- Customer statements

---

## Supplier Management

- Supplier records
- Supplier statements
- Outstanding balances

---

## Sales

- Create invoices
- Issue receipts
- Record customer payments

---

## Purchases

- Record supplier bills
- Record supplier payments

---

## Financial Reports

Generate:

- Trial Balance
- Profit & Loss Statement
- Balance Sheet
- Cash Flow Statement

---

## Dashboard

Display:

- Revenue
- Expenses
- Cash Position
- Outstanding Invoices
- Outstanding Bills
- Recent Transactions

---

# 11. Non-Functional Requirements

The system must be:

## Secure

- Encrypted passwords
- Secure authentication
- Role-based authorization

## Reliable

- Data consistency
- Automatic backups
- Error handling

## Scalable

Support growth in:

- Users
- Transactions
- Companies

## Fast

Typical pages should load within a few seconds under normal usage.

## Maintainable

- Modular architecture
- Clean code
- Documentation
- Automated testing (future)

---

# 12. Technology Stack

## Backend

- Django
- Django REST Framework

## Frontend

- React

## Database

- PostgreSQL

## Authentication

- Django Authentication
- JWT (planned)

## Version Control

- Git
- GitHub

## Deployment (Future)

- AWS

---

# 13. Project Architecture

Frontend (React)

↓

REST API

↓

Django Backend

↓

PostgreSQL Database

---

# 14. Out of Scope (Version 1)

The following features are intentionally excluded from the MVP:

- Payroll
- Inventory
- CRM
- HR
- Fixed Assets
- Budgeting
- Manufacturing
- Mobile Application
- AI Financial Assistant
- Bank Integrations
- M-Pesa Integration
- eTIMS Integration

These will be considered after validating the MVP.

---

# 15. Success Metrics

The MVP will be considered successful if it can:

- Register companies
- Manage users securely
- Record accounting transactions
- Generate accurate financial reports
- Support pilot businesses successfully
- Receive positive user feedback

---

# 16. Risks

Potential risks include:

- Scope creep
- Limited development capacity
- Regulatory changes
- Complex accounting requirements
- Security vulnerabilities
- Changing customer expectations

Mitigation strategies include:

- Prioritizing the MVP
- Regular stakeholder reviews
- Continuous testing
- Incremental feature releases

---

# 17. Future Product Roadmap

The Rozeza platform will evolve into an integrated suite of business applications.

Planned products include:

- Rozeza Ledger
- Rozeza Payroll
- Rozeza Inventory
- Rozeza CRM
- Rozeza HR
- Rozeza Analytics

These products will share a common authentication system, database architecture, and user experience where appropriate.

---

# 18. Founding Team

## Rosemary & Charles

**Co-founders | Product & Engineering Team**

### Responsibilities

- Product Vision & Strategy
- System Architecture
- Backend Development
- Database Design
- REST API Development
- Project Management
- Technical Documentation
- Customer Discovery & Requirements Gathering

---

## Zephaniah

**Co-founder | Head of Finance & Accounting Domain Expert**

Responsibilities:

- Accounting Workflows
- Business Rules
- Financial Controls
- Compliance Guidance
- Product Validation
- User Acceptance Testing

---

# 19. Document Approval

This PRD serves as the guiding document for the Rozeza Ledger MVP.

Major changes to product scope, architecture, or objectives should be discussed by the founding team and recorded in `docs/DECISION_LOG.md`.

---

**End of Document**