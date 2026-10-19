---
name: coding-rules
description: Defines coding standards for Python including naming conventions, architecture patterns, error handling, testing, and AI development rules.
---

# Coding Rules

## 1. Purpose

This skill defines general rules for writing Python code within the project.

The agent must adhere to these rules when:

* Creating new files.
* Modifying existing files.
* Refactoring code.
* Adding new Features.
* Fixing bugs.
* Creating Classes or Functions.
* Adding Services, Repositories, Validators, or Collectors.
* Working with the database.
* Writing user interface code.

The goal is for the code to be:

* Clear.
* Readable.
* Maintainable.
* Testable.
* Extensible.
* Compatible with project Architecture.
* Consistent across all files.

---

# 2. Fundamental Rule

Write the simplest clear code that achieves the requirement.

Do not add:

* Unnecessary Abstractions.
* Classes just for the sake of using Classes.
* Very small Functions without benefit.
* Design Patterns without real need.
* New Dependencies without reason.
* Complexity the project doesn't need.

Complexity must be justified by actual project needs.

---

# 3. Python Version

Must use the Python version specified in project settings.

Before using modern Python features, check:

* `pyproject.toml`
* `requirements.txt`
* Project settings.

Do not use Syntax or APIs not supported by the target version.

---

# 4. Naming Conventions

## 4.1 Files

Use:

```text
snake_case.py
```

Examples:

```text
lead_service.py
company_repository.py
email_validator.py
database_connection.py
```

Avoid:

```text
LeadService.py
leadService.py
lead-service.py
```

---

## 4.2 Variables

Use `snake_case`.

Correct:

```python
company_name = "Example"
lead_status = "new"
email_address = "info@example.com"
```

Incorrect:

```python
companyName = "Example"
LeadStatus = "new"
EmailAddress = "info@example.com"
```

---

## 4.3 Functions

Use `snake_case`.

```python
def find_company_by_domain(domain):
    ...
```

Function names must describe the action they perform.

Good examples:

```python
create_lead()
update_company()
find_contact()
validate_email()
normalize_domain()
export_leads()
```

Avoid ambiguous names:

```python
do_it()
process()
handle()
run()
data()
```

Unless context makes the meaning very clear.

---

# 5. Classes

Use `PascalCase`.

```python
class LeadService:
    ...
```

Examples:

```python
class CompanyRepository:
    ...

class EmailValidator:
    ...

class LeadCollector:
    ...
```

Class name must represent a clear Entity or Responsibility.

---

# 6. Constants

Use `UPPER_SNAKE_CASE`.

```python
DEFAULT_PAGE_SIZE = 50
MAX_EXPORT_ROWS = 10000
DEFAULT_TIMEOUT = 30
```

Place shared Constants in appropriate location like:

```text
config/constants.py
```

And do not create general Constants inside random files.

---

# 7. Boolean Naming

Boolean names must be clear and often start with:

```text
is_
has_
can_
should_
```

Examples:

```python
is_active
is_valid
is_duplicate
has_email
has_domain
can_export
should_retry
```

Avoid:

```python
active
valid
duplicate
```

If the name could cause confusion.

---

# 8. Imports

Organize Imports clearly.

Preferred order:

1. Standard Library
2. Third-party packages
3. Local application imports

Example:

```python
import re
from datetime import datetime
from pathlib import Path

import requests

from app.models.lead import Lead
from app.services.company_service import CompanyService
```

Put a blank line between groups.

---

# 9. Import Rules

Avoid:

```python
from module import *
```

Use clear and specific Imports.

Correct:

```python
from app.models.lead import Lead
```

Instead of:

```python
from app.models.lead import *
```

---

# 10. Circular Imports

Must avoid Circular Imports.

If you need:

```text
A → B → A
```

This often indicates a problem in Architecture or file responsibilities.

Before using solutions like Local Imports inside Functions, first try to solve the problem by reorganizing dependencies.

---

# 11. Type Hints

Use Type Hints in new code, especially in:

* Public Functions.
* Service methods.
* Repository methods.
* Functions dealing with complex data.
* Functions returning Objects.
* Functions where return type may not be obvious.

Example:

```python
def find_company(company_id: int) -> Company | None:
    ...
```

And example:

```python
def normalize_domain(domain: str) -> str:
    ...
```

---

# 12. Return Types

Prefer specifying return type for Functions.

Example:

```python
def get_leads() -> list[Lead]:
    ...
```

Or:

```python
def get_lead(lead_id: int) -> Lead | None:
    ...
```

If Function returns no value:

```python
def delete_lead(lead_id: int) -> None:
    ...
```

---

# 13. Optional Values

If value can be absent, this must be clear in Type Hint.

Example:

```python
def find_contact(email: str) -> Contact | None:
    ...
```

And do not use a dummy value like:

```python
return ""
```

Or:

```python
return 0
```

To represent absence of an Object unless intentionally clear.

---

# 14. Data Structures

Use the simplest appropriate Data Structure.

Use:

```python
list
dict
set
tuple
```

When sufficient.

Do not create a custom Class just to store simple data if there's no actual need for it.

And when data is a core part of the project Domain, use appropriate Models per project Architecture.

---

# 15. Functions

Every Function must be responsible for a clear task.

Good example:

```python
def normalize_domain(domain: str) -> str:
    ...
```

Then:

```python
def find_company_by_domain(domain: str) -> Company | None:
    ...
```

Instead of creating a huge Function that does:

* Clean Domain.
* Connect to database.
* Search.
* Create Company.
* Create Lead.
* Update UI.

In a single Function.

---

# 16. Function Size

No fixed rule for line count.

But if a Function becomes:

* Too long.
* Hard to read.
* Contains multiple independent stages.
* Has many levels of `if`.
* Performs more than one responsibility.

Consider splitting into smaller Functions.

Don't split a Function just to reach a certain line count.

---

# 17. Single Responsibility

Every Module, Class, and Function must have a clear Responsibility.

Example:

```text
Repository
→ Database access

Service
→ Business logic

Validator
→ Validation

Parser
→ Parsing

Collector
→ Data collection

Exporter
→ Export

UI
→ User interaction
```

Do not put Business Logic inside UI.

Do not put SQL inside UI.

Do not make Repository responsible for Business Rules.

---

# 18. Separation of Concerns

Must maintain separation between layers.

General path:

```text
UI
  ↓
Service
  ↓
Repository
  ↓
Database
```

And for data collection:

```text
UI
  ↓
Collector
  ↓
Parser
  ↓
Validator
  ↓
Service
  ↓
Repository
```

Do not bypass layers without a clear architectural reason.

---

# 19. UI Code

UI code is responsible for:

* Displaying data.
* Receiving Input.
* Sending Actions to Services.
* Displaying Errors.
* Displaying Loading/Progress States.

Do not put inside UI:

```python
SQL queries
database transactions
duplicate detection logic
domain normalization logic
lead business rules
scraping logic
```

These responsibilities must remain in appropriate layers.

---

# 20. Database Code

SQL must be in Database/Repository layer per project Architecture.

Avoid:

```python
cursor.execute(...)
```

Inside:

* UI.
* Widgets.
* Pages.
* Dialogs.

Database operations must go through Repository or the layer specified in Architecture.

---

# 21. SQL Parameters

Do not build SQL using String Concatenation.

Avoid:

```python
query = f"SELECT * FROM companies WHERE name = '{name}'"
```

Use Parameterized Queries.

Example:

```python
query = "SELECT * FROM companies WHERE name = ?"
cursor.execute(query, (name,))
```

---

# 22. Error Handling

Do not use:

```python
except:
    pass
```

And do not hide Errors without reason.

Also avoid:

```python
except Exception:
    return None
```

If it hides the problem.

Must handle errors in the appropriate place.

---

# 23. Specific Exceptions

Prefer catching specific Exception when possible.

Example:

```python
try:
    ...
except ValueError:
    ...
```

Instead of:

```python
try:
    ...
except Exception:
    ...
```

Use general `Exception` only when there's an actual need to handle a wide range of errors.

---

# 24. Custom Exceptions

If project needs Domain-specific Errors, can create Custom Exceptions in:

```text
app/core/exceptions.py
```

Example:

```python
class DuplicateLeadError(Exception):
    pass
```

Do not create a Custom Exception for every simple error.

---

# 25. Logging

Use Logging instead of relying on:

```python
print()
```

For important operations or those the system needs to track.

Example:

```python
logger.info("Lead collection started")
logger.warning("Possible duplicate company detected")
logger.error("Failed to save lead")
```

`print()` can be used temporarily during Debugging, but must not remain as a primary Logging mechanism in Production.

---

# 26. Comments

Write Comments when they explain:

* Why a certain solution was chosen.
* Reason for a Workaround.
* A Business Rule not clear from the code.
* Non-intuitive behavior.

Do not write Comments that repeat the code.

Bad:

```python
# Increment counter
counter += 1
```

Better:

```python
# Keep the source record because duplicate detection must remain traceable.
source_records.append(record)
```

---

# 27. Docstrings

Use Docstrings for Public Classes and important Functions when they need to clarify:

* Purpose.
* Complex Parameters.
* Return value.
* Exceptions.
* Business behavior.

Example:

```python
def normalize_domain(domain: str) -> str:
    """Normalize a domain for consistent comparison."""
    ...
```

Do not add huge Docstrings for every simple Function without need.

---

# 28. Avoid Magic Numbers

Avoid mysterious numbers or values inside Logic.

Bad:

```python
if len(results) > 100:
    ...
```

If `100` is an important rule, make it clear:

```python
MAX_RESULTS = 100

if len(results) > MAX_RESULTS:
    ...
```

---

# 29. Avoid Magic Strings

Avoid repeating Status values or Types in multiple places.

Bad:

```python
if lead.status == "qualified":
    ...
```

If these values are used in multiple places, use appropriate Constants or Enum for the Architecture.

Example:

```python
LeadStatus.QUALIFIED
```

But do not create an Enum just for a single value used in one place.

---

# 30. Mutable Default Arguments

Do not use Mutable Objects as Default Arguments.

Avoid:

```python
def collect_leads(leads=[]):
    ...
```

Use:

```python
def collect_leads(leads=None):
    if leads is None:
        leads = []
```

Or appropriate Type/Pattern per case.

---

# 31. Avoid Global Mutable State

Avoid Global Variables that can be modified from multiple places.

Bad:

```python
current_leads = []
```

Then multiple Modules modify it.

Prefer passing data explicitly or using appropriate Service/Repository.

---

# 32. Configuration

Do not put sensitive or changeable project settings inside Business Logic.

Like:

* Database path.
* API keys.
* Timeouts.
* Application settings.
* Export directories.

Must go through appropriate Configuration layer.

---

# 33. Environment Variables

Sensitive information must not be Hardcoded inside code.

Like:

```text
API keys
passwords
tokens
credentials
```

Use Environment Variables or appropriate Configuration mechanism.

Do not put Secrets inside Git.

---

# 34. Path Handling

Use `pathlib` for handling files and paths when appropriate.

Prefer:

```python
from pathlib import Path

data_path = Path("data") / "exports"
```

Instead of manually building paths using String concatenation.

---

# 35. String Handling

Use f-strings when Formatting is needed.

Example:

```python
message = f"Found {count} leads"
```

Avoid building long Strings using repeated `+` operations.

---

# 36. Comparisons

Make comparisons clear.

Example:

```python
if email is None:
    ...
```

Instead of:

```python
if email == None:
    ...
```

And use:

```python
if value:
```

Only when testing Truthiness is actually intended.

---

# 37. Early Returns

Use Early Returns when they make code clearer.

Instead of:

```python
def process_lead(lead):
    if lead:
        if lead.email:
            if lead.is_valid:
                ...
```

Can be:

```python
def process_lead(lead):
    if lead is None:
        return

    if not lead.email:
        return

    if not lead.is_valid:
        return

    ...
```

Do not use Early Returns excessively if they make Logic harder to understand.

---

# 38. Avoid Deep Nesting

Avoid many levels of:

```python
if
    if
        if
            for
                try
```

Split Logic into clear Functions or use Guard Clauses when appropriate.

---

# 39. Loops

Use Pythonic constructs when they make code clearer.

Example:

```python
valid_emails = [
    email
    for email in emails
    if email.is_valid
]
```

But do not use List Comprehension if it becomes complex or less readable than a normal Loop.

---

# 40. Code Duplication

Avoid repeating the same Logic in multiple places.

If real and important Logic repeats, move it to:

* Utility.
* Service.
* Validator.
* Shared Component.

Per responsibility.

But do not create premature Abstraction just for simple similarity.

---

# 41. DRY Principle

Use DRY when it prevents actual Logic duplication.

Do not apply DRY in a way that leads to:

* Overly general Functions.
* Ambiguous Utilities.
* Complex Abstractions.
* Coupling between unrelated Modules.

Clarity is more important than removing every small duplication.

---

# 42. Models

Models must represent data or Domain Entities per project Architecture.

Examples:

```text
Company
Domain
Contact
Email
Lead
```

Do not make Model responsible for:

* UI display.
* Random SQL execution.
* Scraping.
* Exporting.

Unless project's specific Architecture explicitly states otherwise.

---

# 43. Services

Services are responsible for Business Logic.

Example:

```python
class LeadService:
    def create_lead(self, ...):
        ...
```

Service can use:

```text
Repository
Validator
Domain Rules
Models
```

But must not depend on UI widgets.

---

# 44. Repositories

Repository is responsible for data access.

Example:

```python
class CompanyRepository:
    def find_by_domain(self, domain: str) -> Company | None:
        ...
```

Repository must not decide Business Rules like:

```text
Is this Lead ready for outreach?
Should two companies be merged?
Should a Duplicate be deleted?
```

These are Business/Service layer responsibilities.

---

# 45. Validators

Validators are responsible for verifying data validity.

Examples:

```text
EmailValidator
CompanyValidator
LeadValidator
```

Validator must not automatically modify or delete data unless that's a clear part of its function.

---

# 46. Collectors

Collectors are responsible for obtaining data from external Sources.

Like:

```text
Website
Search Engine
Directory
API
Imported File
```

Collector must not contain significant Business Logic for creating Leads.

It can return Raw/Collected Data to the next layers.

---

# 47. Parsers

Parser is responsible for converting raw data into understandable Structure.

Example:

```text
Raw HTML
    ↓
Parser
    ↓
Company data
```

Do not make Parser responsible for saving data to Database.

---

# 48. Exporters

Exporters are responsible for outputting data to:

```text
CSV
Excel
JSON
```

Do not put Business Rules inside Exporter.

---

# 49. Naming Business Methods

Method names must reflect the actual operation.

Examples:

```python
create_company()
find_company_by_domain()
update_company()
detect_duplicate_company()
validate_email()
create_lead()
update_lead_status()
export_leads()
```

Avoid:

```python
process_data()
handle_company()
do_operation()
```

When a more specific name is possible.

---

# 50. No Hidden Side Effects

A Function named:

```python
find_company()
```

Should not secretly:

```text
create company
delete company
modify database
change lead status
```

Function name must reflect its behavior.

Operations that modify data must be explicit.

---

# 51. Data Mutation

Be careful when modifying Objects or Collections used in other places.

If creating a copy is better, do it.

Do not modify a shared Object unexpectedly.

---

# 52. Preserve Existing Behavior

When modifying existing code:

1. Understand current behavior.
2. Inspect Dependencies.
3. Inspect Callers.
4. Determine expected impact.
5. Implement minimal necessary change.
6. Test affected functionality.

Do not rewrite entire Module without need.

---

# 53. Refactoring

When Refactoring:

* Do not change Business Behavior without request.
* Do not mix Refactoring with new Feature unless necessary.
* Preserve Public Interfaces as much as possible.
* Test after change.
* Delete old code only after confirming it's not used.

---

# 54. Backward Compatibility

If changing a Function or Class may affect other parts of the project, inspect all usages first.

Do not change:

```python
def create_lead(data):
```

To:

```python
def create_lead(data, source, user):
```

Without checking all Call Sites and updating them correctly.

---

# 55. Dependencies

Do not add a new Library unless:

* There's an actual need.
* The library is suitable for the project.
* No simple solution exists using Python or existing Dependencies.
* Addition doesn't create unnecessary complexity.

Before adding Dependency, inspect the project first.

---

# 56. Dead Code

Do not leave:

* Unused Imports.
* Unused Functions.
* Unused Variables.
* Unused Classes.
* Debug code.
* Commented-out old implementations.

If you confirm code is no longer used, delete it instead of leaving it as a Comment.

Git is the appropriate place for code history.

---

# 57. Debug Code

Do not leave:

```python
print()
breakpoint()
pdb.set_trace()
```

Or any Debugging code inside Production code unless intentionally clear.

---

# 58. File Responsibility

Do not make a single file contain everything.

Avoid a file like:

```text
utils.py
```

Containing:

```text
Database
Email validation
Lead logic
Date utilities
File operations
UI helpers
Scraping
```

Split responsibilities into clear Modules when the project grows.

---

# 59. Utility Functions

Use Utilities only for general functions that don't clearly belong to a specific Domain.

Appropriate example:

```text
path helpers
date formatting
generic string helpers
```

But:

```text
detect_duplicate_company()
```

Is not a general Utility; it's Business Logic and must be in the appropriate place.

---

# 60. Tests

Any important or error-prone Logic must be testable.

Especially:

* Domain normalization.
* Email normalization.
* Duplicate detection.
* Validation.
* Lead status transitions.
* Business rules.
* Calculations.
* Repository behavior.

Do not make testing Logic require running the full UI if it can be tested in an independent Layer.

---

# 61. Testability

When writing code, think about testability.

Avoid making a Function directly depend on:

```text
global state
UI widgets
hardcoded paths
hardcoded credentials
system time
external services
```

If a dependency or configuration can be passed more clearly, do so.

---

# 62. External Services

Do not let External API or Website dependency spread throughout the project.

Prefer isolating it behind a Collector or appropriate Client.

Example:

```text
External API
    ↓
API Client / Collector
    ↓
Service
```

This makes it easier for:

* Testing.
* Error handling.
* Replacement.
* Maintenance.

---

# 63. Database Transactions

If an operation contains multiple Database operations that must execute as one unit, use Transaction.

Example:

```text
Create Company
+
Create Domain
+
Create Lead
```

If the operation fails in the middle, must not leave Database in an incorrect state.

---

# 64. No Silent Data Loss

Do not write Logic that leads to:

```text
automatic deletion
automatic merge
silent overwrite
```

Especially in:

* Companies.
* Domains.
* Contacts.
* Emails.
* Leads.

Must respect Business Rules in `business-rules.md`.

---

# 65. Data Preservation

When receiving new data, do not replace existing good data with incomplete or lower quality data without reason.

Example:

If we have:

```text
company.website = "https://example.com"
```

And a new empty value arrives:

```text
website = ""
```

Do not automatically replace the good value with the empty value.

---

# 66. Naming Database Variables

When working with Database, use clear names.

Example:

```python
connection
cursor
query
params
row
rows
```

But when context is more specific:

```python
company_row
lead_rows
company_params
```

Is better.

---

# 67. Resource Management

Use Context Managers when appropriate.

Example:

```python
with open(file_path, "r", encoding="utf-8") as file:
    content = file.read()
```

And for Database connections, follow the project's specified Database layer and do not leave Connections open unnecessarily.

---

# 68. Encoding

When handling text files, specify Encoding explicitly when appropriate.

Prefer:

```python
open(file_path, encoding="utf-8")
```

Especially because the application may handle Arabic, French, and English data.

---

# 69. Internationalization

Do not put User-facing text randomly inside Business Logic.

Bad example:

```python
raise Exception("حدث خطأ في البريد الإلكتروني")
```

Prefer messages and translation management in the appropriate layer per `ui-guidelines.md` and Resources.

Business Logic should remain as independent as possible from UI language.

---

# 70. Security

Do not store:

* Passwords.
* API Keys.
* Tokens.
* Secrets.

Inside Source Code.

And do not print Secrets in Logs.

Avoid logging sensitive information without need.

---

# 71. Input Validation

Any data coming from an external source must be considered untrusted until:

```text
Normalize
→ Parse
→ Validate
```

External sources include:

* User Input.
* Websites.
* APIs.
* Imported CSV.
* Excel.
* External files.

---

# 72. External Data

Do not assume external data is:

* Correct.
* Complete.
* Unique.
* Organized.
* Compatible with Database.

Must pass it through appropriate processing stages.

---

# 73. Duplicate Logic

Do not put Duplicate Detection in:

```text
UI
Repository
Database connection
```

Must be within appropriate Business/Service logic.

Must also respect the rule:

```text
Duplicate Detection ≠ Automatic Deletion
```

And:

```text
Possible Duplicate ≠ Confirmed Duplicate
```

---

# 74. Lead Status

Do not put Status values randomly in different files.

Use the central source specified in `project-overview.md` (the canonical Lead Status list) and Business Rules.

Must maintain Lead statuses like:

```text
new
researching
ready
contacted
interested
not_interested
archived
```

And do not change Business Status during technical operations like Validation or Duplicate Detection without a clear reason.

---

# 75. Code Formatting

Must maintain consistent code formatting.

Prefer using the project's adopted Formatter/Linter if it exists.

Do not change Formatting for entire files without need during a small modification.

---

# 76. Small Changes

If the requirement is:

```text
Add Button
```

Do not rewrite:

```text
Entire UI
Services
Repositories
Models
```

Unless necessary.

Apply the minimal change that achieves the requirement.

---

# 77. Inspect Before Editing

Before modifying any file:

1. Read the file.
2. Understand the file's responsibility.
3. Inspect related files.
4. Search for used Functions/Classes.
5. Inspect Business Rules.
6. Inspect Architecture.
7. Execute the modification.
8. Verify no Dependencies are broken.

Do not modify code based solely on the file name.

---

# 78. Follow Existing Project Conventions

If the project already uses a clear Convention, maintain it.

Do not change an existing Convention just because of personal preference.

Before introducing a new Pattern, search for the method currently used in the project.

Consistency is more important than enforcing a new style.

---

# 79. Avoid Premature Optimization

Do not optimize Performance before knowing a real problem exists.

Start with:

```text
Correctness
→ Clarity
→ Maintainability
→ Performance
```

If a Performance problem appears, measure it then optimize the responsible part.

---

# 80. Avoid Premature Abstraction

Do not create:

```text
BaseClass
AbstractFactory
GenericManager
UniversalRepository
```

Just because they might be used in the future.

Create Abstraction when there's a real need, clear duplication, or an architectural requirement.

---

# 81. Keep Dependencies Directional

Dependency direction must be clear.

Example:

```text
UI
  ↓
Services
  ↓
Repositories
  ↓
Database
```

And must not allow a low-level layer to depend on UI layer.

Especially:

```text
Repository → UI
Database → UI
Model → Page
```

These relationships must be avoided.

---

# 82. No Business Logic in Generic Utilities

Do not use:

```text
utils.py
helpers.py
common.py
```

As a place to put any Logic you don't know where to put.

If Logic is specific to Leads, it must be in a Lead-related module.

If it's specific to Companies, it must be in a Company-related module.

---

# 83. Clear Interfaces

When communicating between Modules, Interfaces must be clear.

Example:

```python
company = company_service.get_company(company_id)
```

Better than passing random Objects between layers without a clear Contract.

---

# 84. Avoid Hidden Database Access

Do not make a Model or Utility secretly connect to the database.

Database access must be clear and traceable.

---

# 85. Preserve Traceability

Because the project deals with Lead Generation and external data, must be able to know the data source when the Domain requires it.

Do not delete Source information just to simplify code.

---

# 86. Before Creating a New File

Before creating a new File:

1. Search for an existing File with the same responsibility.
2. Inspect Architecture.
3. Inspect Project Structure.
4. Determine the appropriate layer.
5. Create a new File only if necessary.

Do not create many files without need.

---

# 87. Before Creating a New Class

Ask:

* Is there a Class that can bear this responsibility?
* Is the responsibility truly independent?
* Will the Class be used more than once?
* Does its existence make Architecture clearer?

If the answer is no, use the simplest solution.

---

# 88. Before Creating a New Function

Ask:

* Does the Logic already exist?
* Can an existing Function be reused?
* Does the new Function have a clear Responsibility?
* Does its name accurately express its function?

---

# 89. Code Review Checklist

Before considering a modification complete, verify:

```text
[ ] Clear Naming
[ ] Organized Imports
[ ] Appropriate Type hints
[ ] No unnecessary duplicate code
[ ] No unjustified Magic Values
[ ] No unnecessary Global Mutable State
[ ] No Circular Imports
[ ] No SQL inside UI
[ ] No Business Rules inside Repository
[ ] No UI dependencies inside Business Logic
[ ] No Secrets inside code
[ ] No Debug code
[ ] No hidden Exceptions
[ ] No Dead Code
[ ] Code is testable
[ ] Modification doesn't break Architecture
[ ] Modification doesn't violate Business Rules
```

---

# 90. Rule Priority

When there's a conflict between Coding Rules and other project rules, use this order:

```text
1. Project Architecture
2. Business Rules
3. Database Rules
4. Security Rules
5. Coding Rules
6. Personal coding preference
```

Must not use Coding Rules to override Business Rules or Architecture.

---

# 91. AI Agent Development Rules

When working on the project, the agent must:

1. Read `project-overview.md`.
2. Read `architecture.md`.
3. Read `project-structure.md`.
4. Read `business-rules.md` when modifying Business Logic.
5. Read `database-rules.md` when modifying Database-related code.
6. Read `ui-guidelines.md` when modifying UI.
7. Apply these Coding Rules while writing code.

Before creating or modifying important Code, must understand its correct place in Architecture.

---

# 92. Minimal Change Principle

When executing user request:

```text
Change the minimum amount of code necessary to achieve the requirement.
```

Do not:

* Redesign Architecture without request.
* Rename unrelated files.
* Rewrite entire Modules.
* Add unnecessary Libraries.
* Change Database Schema without need.
* Change unrelated UI behavior.

If an independent problem is discovered during implementation, do not fix it automatically unless it prevents executing the request or fixing it is necessary to maintain the correctness of the modification.

---

# 93. Final Principle

Good code is not the most complex code.

Good code is what another developer can read and understand:

```text
What does it do?
Why does it do it?
Where is the responsibility?
How does data flow?
What does it depend on?
How can it be tested?
```

Therefore priority must always be:

```text
Clarity
→ Correctness
→ Consistency
→ Maintainability
→ Testability
→ Performance

And clarity must not be sacrificed for complexity, Abstraction, or unnecessary Optimization.
