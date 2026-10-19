---
name: project-overview
description: Defines the purpose, scope, goals, core concepts, and boundaries of the domain lead management application.
---

# Project Overview

## 1. Project Identity

This project is a desktop application designed to help domain investors organize and manage prospective customers for domain-name sales.

The application is focused specifically on the workflow of:

```
Domain → Potential Company → Contacts → Contact Information → Lead Management → Outreach Preparation
```

The application is NOT intended to be a general CRM, accounting system, inventory system, or marketing automation platform.

Its primary purpose is to make the collection, organization, review, and management of potential domain buyers simple and efficient.

---

## 2. Main Objective

The main objective of the application is to allow the user to:

1. Store domains that they want to sell.
2. Find and store companies that could potentially be interested in a domain.
3. Associate companies with specific domains.
4. Store information about companies.
5. Store multiple contacts belonging to each company.
6. Store contact information such as emails, phone numbers, and social accounts.
7. Detect possible duplicate companies and contact information.
8. Review and organize leads.
9. Prepare prospect data for future outreach.
10. Search and filter collected information efficiently.
11. Export useful prospect data when needed.

The application should reduce manual organization work and keep prospect information structured.

---

## 3. Target User

The primary user is a domain investor who researches potential buyers for domain names.

The user may collect information from sources such as:

- Company websites
- Search engines
- LinkedIn
- Facebook
- Business directories
- Public business listings
- Manual research
- Other legitimate public sources

The application does not need to perform web scraping or automated lead generation in its first version.

Its primary responsibility is to organize the information collected by the user.

---

## 4. Core Workflow

The fundamental workflow is:

```text
Domain
   ↓
Find potential companies
   ↓
Add company
   ↓
Check for possible duplicates
   ↓
Associate company with domain
   ↓
Add company information
   ↓
Add contacts
   ↓
Add contact information
   ↓
Review lead
   ↓
Prepare for outreach
   ↓
Export if necessary
```

The application should support this workflow naturally through the user interface.

The user should not need to understand the internal database structure in order to use the application.

---

## 5. Core Business Concepts

The application has several important concepts.

### 5.1 Domain

A domain is a domain name that the user owns, controls, or intends to sell.

Examples:

```text
miamielectrician.com
chicagoroofing.com
atlantaplumbing.com
```

A domain is one of the primary entities in the application.

---

### 5.2 Company

A company is a potential buyer or prospect that may be interested in a particular domain.

Examples:

```text
ABC Electric
Miami Electrical Services
Best Roofing Company
```

A company exists independently from a specific domain.

The same company may be a potential buyer for multiple domains.

Therefore, a company must NOT contain a direct `domain_id`.

The relationship between companies and domains is handled separately.

---

### 5.3 Domain Lead

A Domain Lead represents the relationship between a domain and a company.

Example:

```text
Domain:
miamielectrician.com

Company:
ABC Electric
```

This relationship means:

```text
ABC Electric
may be a potential buyer
of
miamielectrician.com
```

The same company may therefore have multiple Domain Lead relationships:

```text
ABC Electric
   ├── miamielectrician.com
   ├── miamielectrical.com
   └── miamielectricservices.com
```

Lead-specific information such as status, priority, and notes belongs to the Domain Lead relationship, not directly to the Company.

---

## 6. Company Information

A company may contain:

* Company name
* Website
* Description
* Address
* City
* State
* Country
* Company emails
* Company phone numbers
* Company social accounts
* Contacts

The application should allow a company to have multiple pieces of contact information.

---

## 7. Contacts

A contact represents a real person working for a company.

Examples:

```text
John Smith
Michael Johnson
Sarah Williams
```

A company may have multiple contacts.

Example:

```text
ABC Electric
   ├── John Smith
   ├── Sarah Williams
   └── Michael Johnson
```

A contact may have:

* First name
* Last name
* Full name
* Job title
* Department
* Notes
* Email addresses
* Phone numbers
* Social accounts

---

## 8. Email Ownership Rule

This is a critical business rule.

A contact email belongs to ONE person only.

For example:

```text
john@abcelectric.com
        ↓
     John Smith
```

The same email must NOT be assigned to:

```text
John Smith
AND
Michael Johnson
```

The application must detect this situation and prevent duplicate ownership.

Contact emails are different from company emails.

Example:

```text
Company email:

info@abcelectric.com
sales@abcelectric.com


Contact email:

john@abcelectric.com
sarah@abcelectric.com
```

However, the same normalized email must not exist simultaneously as both a company email and a contact email.

The application must check both types before saving an email.

---

## 9. Company Emails

Company emails represent addresses belonging to the business rather than a specific individual.

Examples:

```text
info@company.com
sales@company.com
support@company.com
marketing@company.com
```

A company may have multiple company emails.

Company emails should not be confused with personal/contact emails.

---

## 10. Duplicate Detection

Duplicate detection is a major feature of the application.

The application must distinguish between:

```text
Exact duplicate
Strong duplicate
Possible duplicate
```

### 10.1 Exact Duplicate

An exact duplicate is information that is clearly already present.

Examples:

```text
Same normalized domain
Same normalized email
Same domain + same company relationship
```

Exact duplicates should normally be prevented.

---

### 10.2 Strong Duplicate

A strong duplicate is information that strongly suggests that two records represent the same entity.

Examples:

```text
Same website
Same phone number
Same social URL
```

The application should warn the user.

It should NOT automatically delete or merge records.

---

### 10.3 Possible Duplicate

A possible duplicate is information that may represent the same company but cannot be confirmed automatically.

Examples:

```text
ABC Electric

ABC Electrical Services

ABC Electric LLC
```

The application may suggest that these records could represent the same company.

The user must make the final decision.

---

## 11. Duplicate Handling Philosophy

The application follows this principle:

```text
Detect
   ↓
Suggest
   ↓
Review
   ↓
User decides
```

The application must NOT automatically:

* Delete companies
* Merge companies
* Delete contacts
* Delete emails
* Replace existing information

unless the user explicitly performs that action.

The system should prioritize data preservation.

---

## 12. Normalization

Normalization is used to compare data reliably.

The application should preserve the original user-entered value while maintaining a normalized value for comparisons.

### Email normalization

At minimum:

```text
Trim whitespace
Convert to lowercase
```

Example:

```text
John@Example.com
john@example.com
 JOHN@EXAMPLE.COM
```

should be treated as the same email for duplicate detection.

---

### Domain normalization

Domain names should be normalized so that case differences do not create duplicates.

Example:

```text
MiamiElectrician.com
miamielectrician.com
MIAMIELECTRICIAN.COM
```

should be treated as the same domain.

---

### Website normalization

Website normalization should remove irrelevant differences such as:

```text
http://
https://
www.
trailing slash
```

when appropriate for comparison.

Example:

```text
https://www.example.com/
www.example.com
example.com
```

should normally be recognized as the same website.

---

### Phone normalization

Phone numbers should be normalized for comparison while preserving the original displayed number.

Different formatting should not automatically be treated as different numbers.

Example:

```text
+213 555 123 456
+213-555-123-456
+213555123456
```

may represent the same phone number.

---

### Social URL normalization

Social URLs should also be normalized where appropriate so that obvious URL variations can be detected.

---

## 13. Lead Status (Canonical List)

Each Domain Lead can have a status.

> **📌 Canonical Lead Status List for this project:**
> The Lead Status values defined here are the canonical source of truth.
> All other skills (especially `business-rules.md`) must use this exact list.
> Do NOT introduce alternative status values (such as Qualified, Negotiating, Won, Lost)
> unless explicitly required by the user.

The Lead statuses are:

```text
new
researching
ready
contacted
interested
not_interested
archived
```

Meaning:

#### new

The company has recently been added and has not been researched or processed yet.

#### researching

The user is still researching the company or its contacts.

#### ready

The lead has enough information and is ready for outreach.

This does not mean that an email has been sent.

#### contacted

The user has already contacted the company.

The application does not need to send the message itself in the first version.

#### interested

The company has shown interest in the domain.

#### not_interested

The company has been determined not to be interested.

#### archived

The lead is no longer active but should remain in the database for historical reference.

These statuses belong to the Domain Lead, not the Company.

---

## 14. Lead Priority

Each Domain Lead may have a priority:

```text
low
normal
high
```

Priority is specific to the relationship between the company and domain.

A company can therefore have:

```text
Domain A → High priority

Domain B → Normal priority
```

without changing the company itself.

---

## 15. Data Preservation

The application should favor preserving collected information.

When information conflicts, the system should not silently overwrite useful existing information.

For example:

Existing:

```text
Company:
ABC Electric

Phone:
+1 555 111 1111
```

New information:

```text
Phone:
+1 555 222 2222
```

The application should normally allow both numbers to exist rather than replacing the old number automatically.

The user can decide which one is primary.

---

## 16. Primary Information

Some entities can have multiple contact values.

Examples:

```text
Company:
    multiple emails
    multiple phones

Contact:
    multiple emails
    multiple phones
```

The application may mark one value as:

```text
is_primary = 1
```

All other values should normally have:

```text
is_primary = 0
```

The application should ensure that changing the primary value does not accidentally delete the other values.

---

## 17. Application Scope (V1)

The first version should focus on:

* Domain management
* Company management
* Contact management
* Email management
* Phone management
* Social account management
* Lead status (using the canonical 7 statuses)
* Lead priority
* Duplicate detection
* Search
* Filtering
* Basic export
* Notes
* Data organization

---

## 18. Features NOT Required in the First Version

Do not introduce unnecessary features unless explicitly requested.

The first version does NOT need:

* Complex dashboards
* Advanced analytics
* Complicated charts
* Sales forecasting
* Revenue calculations
* Accounting
* Inventory management
* Payment processing
* Email sending automation
* Mass email campaigns
* Complex CRM automation
* AI lead scoring
* Web scraping
* Browser automation
* Multi-user permissions
* Enterprise-level features

The application should remain focused and lightweight.

---

## 19. User Interface Philosophy

The interface should be:

* Simple
* Clean
* Professional
* Fast
* Easy to understand
* Visually organized
* Consistent

The application should prioritize usability over visual complexity.

Avoid unnecessary:

* Charts
* Graphs
* Decorative dashboards
* Excessive animations
* Complicated navigation
* Large numbers of modal dialogs

Every screen should have a clear purpose.

---

## 20. Search

The application should make it easy to search collected information.

The user should eventually be able to search by:

```text
Domain
Company name
Website
Email
Contact name
Phone
```

Search should be fast and should not require the user to know database terminology.

---

## 21. Export

The application should support exporting useful prospect information.

A typical export may contain:

```text
Domain
Company
Contact
Job Title
Email
Website
Phone
City
State
Country
Lead Status
Lead Priority
```

The exact export structure can evolve later.

---

## 22. Database

The application uses:

```text
SQLite
```

The database is local to the desktop application.

The first version does not require:

```text
MySQL
PostgreSQL
SQL Server
```

or another external database server.

The SQLite database should be stored in the application's data area.

Example:

```text
data/
└── leads.db
```

The application must enable SQLite foreign-key enforcement.

---

## 23. Data Access Philosophy

The UI must NOT directly execute SQL queries.

The preferred flow is:

```text
UI
  ↓
Service
  ↓
Repository
  ↓
SQLite
```

The UI is responsible for presentation and user interaction.

Services contain business logic.

Repositories handle data access.

The database layer handles SQLite-specific operations.

This separation must be maintained throughout the project.

---

## 24. Application Architecture

The application should use a clear layered architecture.

Conceptually:

```text
Presentation Layer
        ↓
Service / Business Layer
        ↓
Repository / Data Access Layer
        ↓
Database
```

Shared utilities and infrastructure should remain separated from business logic.

Do not allow random dependencies between unrelated layers.

---

## 25. Important Architectural Principle

The database schema must NOT dictate the UI structure.

For example, the existence of:

```text
company_emails
company_phones
company_socials
```

does not mean the UI must display three separate complicated screens.

The UI should be designed around the user's workflow.

The database exists to store structured information.

---

## 26. Company and Domain Separation

Never assume:

```text
One Company = One Domain
```

This is incorrect.

The correct model is:

```text
Company
   ↕
Domain Lead
   ↕
Domain
```

A company may be associated with many domains.

A domain may have many potential companies.

The `domain_leads` relationship is therefore essential.

---

## 27. Company and Contact Separation

Never store multiple contacts directly as columns inside the company table.

Incorrect:

```text
company
    contact1_name
    contact2_name
    contact3_name
```

Correct:

```text
companies
    ↓
contacts
```

A company may have any number of contacts.

---

## 28. Contact and Email Separation

Never store contact emails as multiple columns such as:

```text
email1
email2
email3
```

Instead:

```text
contacts
    ↓
contact_emails
```

This allows an arbitrary number of emails while maintaining proper relationships.

---

## 29. Company and Contact Social Accounts

Social accounts should remain flexible.

Do not create a separate database column for every possible social platform.

Avoid structures such as:

```text
facebook
linkedin
instagram
twitter
youtube
...
```

Instead use a flexible structure containing:

```text
platform
url
```

This allows new platforms to be supported without changing the database schema.

---

## 30. General Development Philosophy

The application should be developed incrementally.

Each feature should be:

1. Designed
2. Implemented
3. Tested
4. Reviewed
5. Integrated

Do not implement large amounts of unrelated functionality at once.

Prefer small, understandable changes.

---

## 31. Change Safety

Before changing an existing feature:

1. Understand the current implementation.
2. Identify dependencies.
3. Determine whether database changes are required.
4. Determine whether services or repositories are affected.
5. Determine whether the UI is affected.
6. Make the smallest appropriate change.
7. Test the affected functionality.

Never make broad architectural changes merely to solve a small problem.

---

## 32. Final Project Principle

The most important principle of this project is:

```text
Keep the application simple,
keep the data structured,
preserve collected information,
detect duplicates intelligently,
and let the user make important decisions.

The application should help the user organize domain-sales prospects, not become an unnecessarily complicated CRM.

Every technical and UI decision should be evaluated against this principle.
