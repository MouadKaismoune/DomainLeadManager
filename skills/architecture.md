---
name: architecture
description: Defines the software architecture, application layers, responsibilities, dependency direction, communication rules, and separation of concerns for the domain lead management desktop application.
---

# Architecture Skill

## 1. Purpose

This skill defines the software architecture of the application.

The application must use a layered architecture that clearly separates:

- User Interface
- Business Logic
- Data Access
- Database
- Shared Infrastructure

The purpose of this architecture is to make the application:

- Easy to understand
- Easy to maintain
- Easy to test
- Easy to extend
- Resistant to duplicated logic
- Resistant to tightly coupled components

Codex must follow this architecture whenever creating, modifying, or refactoring code.

---

# 2. Architectural Principle

The application follows this general flow:

```text
User
  ↓
UI Layer
  ↓
Service / Business Layer
  ↓
Repository Layer
  ↓
SQLite Database
````

Shared utilities and infrastructure support the appropriate layers without becoming a place for arbitrary business logic.

The dependency direction must generally move downward:

```text
UI
 ↓
Services
 ↓
Repositories
 ↓
Database
```

Lower layers must not depend on higher layers.

For example:

```text
Repository → UI
```

is forbidden.

And:

```text
Service → UI
```

is forbidden.

---

# 3. High-Level Architecture

The recommended architecture is:

```text
Application
│
├── Presentation / UI
│
├── Services / Business Logic
│
├── Repositories / Data Access
│
├── Database
│
└── Shared / Infrastructure
```

A more detailed representation:

```text
┌──────────────────────────────┐
│          UI Layer            │
│ Windows / Views / Forms      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Service Layer           │
│ Business Rules / Validation  │
│ Workflows / Transactions     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Repository Layer        │
│ CRUD / Queries / Persistence │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        SQLite Database       │
└──────────────────────────────┘

       Shared / Infrastructure
       supports the application
```

---

# 4. UI Layer

The UI layer is responsible for interaction with the user.

It includes things such as:

* Windows
* Pages
* Forms
* Dialogs
* Tables
* Buttons
* Input fields
* Navigation
* UI-specific formatting
* Displaying validation errors
* Displaying success/error messages

The UI layer must focus on presentation and user interaction.

It must NOT contain database queries or important business rules.

---

# 5. UI Responsibilities

The UI may:

1. Display data.
2. Collect user input.
3. Perform simple UI-level checks.
4. Call the appropriate Service.
5. Display Service results.
6. Display errors.
7. Refresh the relevant view.
8. Control navigation.

Example:

```text
User clicks "Add Company"
        ↓
Company Form collects input
        ↓
UI calls CompanyService
        ↓
CompanyService validates and processes
        ↓
CompanyRepository saves the company
        ↓
Service returns result
        ↓
UI displays success
```

The UI should not directly execute SQL.

---

# 6. What the UI Must NOT Do

The UI must NOT:

* Open SQLite connections directly for business operations.
* Execute SQL queries.
* Contain repository implementations.
* Implement complex business rules.
* Perform database transactions manually.
* Duplicate validation logic used by services.
* Decide how database records are stored.
* Manipulate database tables directly.

Forbidden example:

```python
class CompanyWindow:
    def save_company(self):
        connection = sqlite3.connect(...)
        connection.execute(
            "INSERT INTO companies (...) VALUES (...)"
        )
```

This creates tight coupling between UI and database.

Instead:

```python
class CompanyWindow:
    def save_company(self):
        result = company_service.create_company(...)
```

The service controls the operation.

---

# 7. Service / Business Layer

The Service layer contains the application's business logic.

This is one of the most important layers.

It is responsible for:

* Business rules
* Workflows
* Validation
* Duplicate detection
* Normalization decisions
* Coordinating repositories
* Transactions
* Business-level error handling
* Enforcing relationships between entities

Examples:

```text
DomainService
CompanyService
ContactService
LeadService
EmailService
PhoneService
SocialService
```

The exact service structure may evolve as the application grows.

---

# 8. Service Layer Responsibilities

A Service may:

1. Validate business requirements.
2. Normalize values when required.
3. Check for duplicates.
4. Call one or more repositories.
5. Coordinate multiple operations.
6. Start or participate in transactions.
7. Enforce business rules.
8. Return structured results to the UI.

Example:

```text
UI
 ↓
CompanyService.create_company()
 ↓
Normalize company data
 ↓
Check duplicate company
 ↓
Validate required information
 ↓
CompanyRepository.insert()
 ↓
Return result
```

---

# 9. Business Logic Must Live in Services

Business rules must not be duplicated across UI screens.

For example:

```text
A contact email belongs to one contact.
```

This is a business rule.

It should be enforced by the Service layer and appropriate database constraints.

Another example:

```text
A domain-company pair can only represent one Domain Lead.
```

This is a business rule.

The Service should respect this rule.

---

# 10. Repository Layer

The Repository layer is responsible for persistence and database access.

Repositories communicate with SQLite.

Examples:

```text
DomainRepository
CompanyRepository
LeadRepository
ContactRepository
CompanyEmailRepository
ContactEmailRepository
CompanyPhoneRepository
ContactPhoneRepository
CompanySocialRepository
ContactSocialRepository
```

Repositories should contain database-related operations rather than business workflows.

---

# 11. Repository Responsibilities

A repository may:

* Insert records
* Update records
* Delete records
* Retrieve records
* Search records
* Filter records
* Execute SQL queries
* Map database rows to application objects/data structures
* Handle persistence-related operations

Example:

```python
company_repository.create(company)
company_repository.get_by_id(company_id)
company_repository.search(query)
company_repository.update(company)
company_repository.delete(company_id)
```

The repository should not decide whether a company is strategically a good lead.

That is business logic and belongs to the Service layer.

---

# 12. What the Repository Must NOT Do

The Repository must not:

* Display UI messages.
* Open UI windows.
* Depend on UI classes.
* Decide business workflows.
* Perform unrelated business decisions.
* Contain presentation logic.
* Automatically merge business entities.

Forbidden:

```python
class CompanyRepository:
    def create(self, company):
        if company_is_high_value_lead(company):
            ...
```

The repository should focus on persistence.

---

# 13. Database Layer

SQLite is the persistence technology used by the application.

The database stores persistent application data.

The database is responsible for:

* Tables
* Columns
* Primary keys
* Foreign keys
* Unique constraints
* Indexes
* Database-level integrity
* Transactions at the database level

The application uses:

```text
Python
   ↓
Repository
   ↓
SQLite
```

The UI must never communicate directly with SQLite.

---

# 14. Database Is Not the Business Layer

The database schema defines how data is stored.

It does not define the entire business logic.

For example:

```text
companies
contacts
domains
domain_leads
```

are database structures.

But the meaning of:

```text
"ready"
"interested"
"high priority"
```

belongs to the application's business domain.

The Service layer should interpret and enforce business behavior.

---

# 15. Shared / Infrastructure Layer

Shared infrastructure contains functionality used by multiple parts of the application.

Examples may include:

```text
Database connection management
Configuration
Logging
Exceptions
Normalization utilities
Common helpers
Application constants
```

Shared code must remain focused and reusable.

Do not turn a generic `utils` module into a dumping ground for unrelated code.

---

# 16. Dependency Direction

The dependency direction must remain predictable.

Preferred:

```text
UI
 ↓
Services
 ↓
Repositories
 ↓
Database
```

Shared infrastructure may be used where appropriate.

For example:

```text
UI ───────────────→ Services
                       │
                       ├──→ Repositories
                       │
                       └──→ Shared
                               
Repositories ─────→ Database / Infrastructure
```

Avoid circular dependencies.

---

# 17. Forbidden Dependency Direction

The following patterns are forbidden:

```text
Repository → UI
```

```text
Database → Service
```

```text
Database → UI
```

```text
UI → Database
```

for normal application operations.

Also avoid:

```text
Service A → UI B
```

or:

```text
Service → Window
```

Services should return results/errors rather than opening windows themselves.

---

# 18. UI-to-Service Communication

The UI communicates with the Service layer through explicit methods.

Example:

```python
company_service.create_company(...)
```

The UI should not know how the company is stored.

The UI only needs to know:

* What operation it wants.
* What input is required.
* What result is returned.
* How to display that result.

Example flow:

```text
Company Form
     │
     │ create_company(data)
     ▼
CompanyService
     │
     │ repository.create(...)
     ▼
CompanyRepository
     │
     ▼
SQLite
```

---

# 19. Service-to-Repository Communication

Services use repositories to access persistent data.

Example:

```text
CompanyService
      │
      ├── CompanyRepository
      │
      └── CompanyEmailRepository
```

A service may coordinate multiple repositories when a business operation requires multiple records.

Example:

```text
Create Company + Add Company Email
```

The Service may coordinate:

```text
CompanyRepository
        +
CompanyEmailRepository
```

inside one appropriate transaction.

---

# 20. Repository-to-Database Communication

Repositories communicate with SQLite.

Repositories should use parameterized SQL.

Never construct SQL by directly concatenating user input.

Forbidden:

```python
sql = f"SELECT * FROM companies WHERE name = '{name}'"
```

Preferred:

```python
cursor.execute(
    "SELECT * FROM companies WHERE name = ?",
    (name,)
)
```

All database operations must remain safe and predictable.

---

# 21. Transactions

Transactions belong to business operations that require multiple database changes to succeed together.

For example:

```text
Create company
+
Create company email
```

If both operations are logically one business operation, they should be handled atomically.

Conceptually:

```text
BEGIN
    Create Company
    Create Email
COMMIT
```

If something fails:

```text
ROLLBACK
```

The Service layer should coordinate transaction boundaries.

Repositories should not independently commit every individual operation when those operations form one larger business transaction.

---

# 22. Example: Creating a Company

Correct architecture:

```text
User
 ↓
Company Form
 ↓
CompanyService.create_company()
 ↓
Validate company information
 ↓
Normalize relevant values
 ↓
Check duplicate conditions
 ↓
CompanyRepository.create()
 ↓
SQLite
 ↓
Return result
 ↓
Company Form displays result
```

The UI does not know the SQL.

The Repository does not know how the UI works.

The Service coordinates the operation.

---

# 23. Example: Creating a Lead

A Domain Lead connects a domain and company.

Correct flow:

```text
User
 ↓
Lead UI
 ↓
LeadService.create_lead()
 ↓
Validate domain and company
 ↓
Check existing domain-company relationship
 ↓
Create Domain Lead
 ↓
LeadRepository.create()
 ↓
SQLite
 ↓
Return result
 ↓
UI refreshes lead list
```

The unique domain-company relationship must be respected.

---

# 24. Example: Adding a Contact Email

Correct flow:

```text
Contact UI
 ↓
ContactService.add_email()
 ↓
Validate email
 ↓
Normalize email
 ↓
Check email conflicts
 ↓
ContactEmailRepository.create()
 ↓
SQLite
 ↓
Return result
 ↓
UI displays the new email
```

The Service handles the business rule.

The Repository handles persistence.

The UI handles presentation.

---

# 25. Validation Responsibility

Validation can exist at multiple levels, but responsibilities must remain clear.

## UI Validation

Simple immediate feedback.

Examples:

```text
Required field is empty
Invalid input format
```

## Service Validation

Business validation.

Examples:

```text
Domain does not exist
Company does not exist
Duplicate lead
Invalid lead status
Invalid priority
Email ownership conflict
```

## Database Constraints

Data integrity.

Examples:

```text
Primary key
Foreign key
Unique constraint
NOT NULL
```

The same rule should not be unnecessarily duplicated in many places.

---

# 26. Error Handling Across Layers

Errors should move upward in a controlled way.

Example:

```text
SQLite error
    ↓
Repository
    ↓
Service
    ↓
UI
    ↓
User-friendly message
```

The UI should not expose raw database errors unless necessary for debugging.

For example, instead of displaying:

```text
sqlite3.IntegrityError: UNIQUE constraint failed...
```

the UI should display an appropriate user-facing message such as:

```text
This email already exists.
```

The underlying technical error may still be logged.

---

# 27. Return Values

Services should return meaningful results.

Possible patterns include:

```text
Success
Failure
Created object
Updated object
Validation error
Business error
```

The exact implementation pattern may be decided during coding, but it must remain consistent throughout the application.

Avoid random return conventions between services.

For example, do not have:

```text
Service A → True/False
Service B → None
Service C → Dictionary
Service D → Exception
```

without a clear reason.

---

# 28. Navigation Responsibility

Navigation belongs to the UI layer.

For example:

```text
Open Company Details
Open Contact Details
Open Lead Details
Return to Lead List
```

These are presentation concerns.

A Service must not directly navigate between windows.

Forbidden:

```python
def create_company(...):
    ...
    company_window.open()
```

Preferred:

```text
Service returns result
        ↓
UI decides what to display or where to navigate
```

---

# 29. UI Refresh Responsibility

After a successful operation, the UI decides how to refresh itself.

Example:

```text
User creates company
        ↓
CompanyService.create_company()
        ↓
Success
        ↓
UI refreshes company list
```

The Service should not directly manipulate UI widgets.

---

# 30. Shared Models / Data Structures

If the application uses domain models, DTOs, or similar structures, they must have a clear purpose.

Possible examples:

```text
Domain
Company
DomainLead
Contact
Email
Phone
Social
```

These structures should represent business data rather than UI widgets or database cursors.

Do not pass UI objects deep into the Service or Repository layers.

Forbidden:

```python
company_service.create_company(company_form_widget)
```

Preferred:

```python
company_service.create_company(company_data)
```

---

# 31. Avoid God Classes

Do not create one class responsible for everything.

Forbidden example:

```text
ApplicationManager
    ├── UI
    ├── Database
    ├── SQL
    ├── Validation
    ├── Business Rules
    ├── Navigation
    ├── Logging
    └── Export
```

This creates a highly coupled system.

Responsibilities should be divided according to the architecture.

---

# 32. Avoid God Services

Do not create one massive service such as:

```text
LeadService
```

that contains every possible operation in the application.

If the service becomes too large, divide responsibilities logically.

Possible separation:

```text
DomainService
CompanyService
ContactService
LeadService
EmailService
PhoneService
SocialService
```

The exact boundaries should be based on actual business responsibilities rather than creating unnecessary abstractions.

---

# 33. Avoid Premature Abstraction

Do not create abstractions simply because they look architecturally sophisticated.

Avoid unnecessary:

* Factories
* Interfaces
* Abstract base classes
* Dependency injection frameworks
* Generic repositories
* Complex event systems
* Excessive design patterns

unless they solve a real problem in the project.

The architecture should be professional but practical.

---

# 34. No Business Logic in SQL

SQL may perform database-level operations and constraints.

However, important business workflows should not be hidden inside complicated SQL.

For example, determining whether a company is a suitable domain buyer should not be implemented as a complex database query unless there is a specific justified requirement.

Business decisions belong primarily in Python's Service layer.

---

# 35. No SQL in UI

This is a strict rule.

The UI must never contain SQL queries.

Forbidden:

```python
cursor.execute(...)
connection.execute(...)
SELECT ...
INSERT ...
UPDATE ...
DELETE ...
```

inside UI classes.

All persistence must go through repositories/services.

---

# 36. No UI Logic in Repositories

Repositories must never contain:

```python
messagebox.showinfo(...)
window.close()
widget.setText(...)
```

or similar UI operations.

Repositories return data/results.

The UI decides how to present them.

---

# 37. No Database Logic in Services

Services should not become collections of raw SQL.

Avoid:

```python
class CompanyService:
    def create_company(self):
        connection = sqlite3.connect(...)
        connection.execute(...)
```

Instead:

```python
class CompanyService:
    def create_company(self, data):
        ...
        return self.company_repository.create(data)
```

The Repository owns persistence details.

---

# 38. Search Architecture

Search operations should follow the same architecture.

Example:

```text
Search UI
 ↓
Search Service
 ↓
Repository
 ↓
SQLite
 ↓
Results
 ↓
UI
```

The UI may collect:

```text
Search term
Status
Priority
Domain
Company
```

The Service may validate and coordinate the search.

The Repository executes the appropriate database query.

---

# 39. Filtering Architecture

Filtering follows the same principle.

Example:

```text
Lead List UI
 ↓
LeadService.search(...)
 ↓
LeadRepository.search(...)
 ↓
SQLite
```

Filtering must not result in duplicated SQL scattered across multiple UI screens.

---

# 40. Export Architecture

Export is an application feature and should respect the architecture.

Example:

```text
Export UI
 ↓
Export Service
 ↓
Lead / Company Repository
 ↓
Data
 ↓
Export Service
 ↓
CSV / Excel / Other supported format
```

The UI should not directly query the database simply to export data.

The exact export formats may evolve later.

---

# 41. Logging Architecture

Logging should be available to relevant layers without coupling them to the UI.

For example:

```text
Service
 ↓
Logger
```

or:

```text
Repository
 ↓
Logger
```

Logs should help diagnose:

* Unexpected errors
* Database failures
* Important application events
* Failed operations

Do not use logging as a replacement for proper error handling.

---

# 42. Configuration

Configuration should be centralized.

Examples:

```text
Database path
Application settings
Logging configuration
Export settings
```

Do not hard-code configuration values throughout the application.

Avoid:

```python
sqlite3.connect("/home/user/project/database/app.db")
```

in multiple files.

Use a centralized configuration mechanism.

---

# 43. Database Connection Management

Database connection management should be centralized.

UI screens should not independently create random database connections.

Repositories should use the application's database infrastructure.

The architecture should make it clear:

```text
Application
    ↓
Database Infrastructure
    ↓
SQLite Connection
```

This makes connection handling easier to maintain and test.

---

# 44. Testing Architecture

The architecture must allow layers to be tested independently.

Examples:

## Service Tests

Test:

```text
Business rules
Validation
Duplicate detection
Workflows
```

## Repository Tests

Test:

```text
Database operations
Queries
Persistence
Constraints
```

## UI Tests

Test:

```text
User interaction
Presentation behavior
Navigation
```

The goal is to avoid requiring the entire application to run just to test a small business rule.

---

# 45. Architecture and Testability

Good architecture should allow this:

```text
Test CompanyService
        ↓
Mock/Fake Repository
```

instead of:

```text
Test CompanyService
        ↓
Open UI
        ↓
Open Database
        ↓
Click Buttons
        ↓
Check Result
```

Not every test needs to use the UI or a real database.

---

# 46. Dependency Injection

Simple dependency injection may be used when useful.

For example:

```python
class CompanyService:
    def __init__(self, company_repository):
        self.company_repository = company_repository
```

This can make testing easier.

However, do not introduce a complex dependency injection framework unless the project actually requires it.

Simple explicit dependencies are preferred.

---

# 47. Circular Dependencies

Circular dependencies are forbidden unless there is an exceptionally strong architectural reason.

Avoid:

```text
CompanyService
   ↓
ContactService
   ↓
CompanyService
```

Avoid:

```text
UI A
 ↓
UI B
 ↓
UI A
```

Avoid:

```text
Repository A
 ↓
Repository B
 ↓
Repository A
```

If circular dependencies appear, reconsider the responsibility boundaries.

---

# 48. Module Boundaries

Modules should be organized according to responsibility.

A possible structure is:

```text
src/
├── ui/
├── services/
├── repositories/
├── models/
├── database/
├── infrastructure/
└── main.py
```

The exact folder structure may evolve, but the architectural responsibilities must remain clear.

Do not move code between folders merely for visual organization if doing so violates architectural responsibility.

---

# 49. Feature-Based Organization

As the application grows, feature-oriented organization may be considered.

For example:

```text
companies/
    ui/
    services/
    repositories/

contacts/
    ui/
    services/
    repositories/

domains/
    ui/
    services/
    repositories/
```

However, this should only be introduced if the project becomes large enough to benefit from it.

For the initial version, a clear layered structure is preferred because simplicity is more valuable than unnecessary structural complexity.

---

# 50. Architecture Rule for Codex

Before implementing any feature, Codex must determine:

1. Which layer owns the feature?
2. Which business entity does it affect?
3. Does it require business logic?
4. Does it require database access?
5. Which Service should coordinate it?
6. Which Repository should persist or retrieve the data?
7. What should the UI display?
8. Does the operation require a transaction?
9. Does the change introduce a dependency violation?
10. Can the feature be tested independently?

Do not begin coding until these responsibilities are clear.

---

# 51. Feature Implementation Flow

For a typical new feature, Codex should follow:

```text
1. Understand the business requirement
        ↓
2. Identify affected entities
        ↓
3. Identify business rules
        ↓
4. Decide Service responsibility
        ↓
5. Decide Repository responsibility
        ↓
6. Decide UI responsibility
        ↓
7. Implement database changes if required
        ↓
8. Implement Repository
        ↓
9. Implement Service
        ↓
10. Implement UI
        ↓
11. Add validation and error handling
        ↓
12. Test the feature
```

Do not start by writing UI code simply because the feature is visible.

---

# 52. Architecture Decision Rule

When there are multiple possible implementations, prefer the solution that:

1. Keeps responsibilities separated.
2. Minimizes coupling.
3. Keeps business logic outside the UI.
4. Keeps SQL outside the UI and Service layer.
5. Keeps persistence inside repositories.
6. Keeps navigation inside the UI.
7. Is easy to test.
8. Is simple enough for the project's actual size.
9. Does not introduce unnecessary abstractions.
10. Preserves the existing architecture.

---

# 53. Refactoring Rule

When modifying existing code, Codex must not blindly preserve a bad architectural decision.

If existing code violates the architecture, Codex should:

1. Identify the violation.
2. Explain its impact if relevant.
3. Refactor it carefully.
4. Preserve existing functionality.
5. Avoid unrelated rewrites.

Do not rewrite the entire application simply to make a small architectural improvement.

Refactoring must remain focused.

---

# 54. Architecture Integrity

Every layer must have a clear reason to exist.

Use this rule:

```text
UI
→ presentation and interaction

Service
→ business behavior and workflows

Repository
→ persistence and database queries

Database
→ persistent storage and data integrity

Infrastructure
→ shared technical capabilities
```

If code does not clearly belong to one responsibility, stop and determine its correct architectural location before implementing it.

---

# 55. Final Architecture Principle

The application must remain simple enough to understand while maintaining professional separation of responsibilities.

The fundamental rule is:

```text
UI
    ↓
Service
    ↓
Repository
    ↓
SQLite
```

With shared infrastructure supporting the application where necessary.

The UI should never become the database layer.

The Repository should never become the business layer.

The Service should never become the UI.

The Database should never become the application's entire business logic.

Codex must preserve this separation throughout development.
