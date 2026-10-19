---
name: project-structure
description: Defines the standard project structure for the Lead Generation Application, specifying the location of each code type and resource with clear responsibilities for each folder.
---

# Project Structure Skill

## Purpose

This skill defines the standard structure for the Lead Generation Application project, and clarifies where each type of code, files, and resources should be placed.

The agent must adhere to this structure when creating new files or modifying existing ones.

The goal of this structure is:

- Separate responsibilities between parts of the program.
- Prevent placing business logic inside the graphical interface.
- Prevent placing database queries inside the interface.
- Facilitate project maintenance and development.
- Facilitate testing each part independently.
- Make the project extensible.
- Avoid huge files containing multiple responsibilities.
- Maintain clear organization between the interface, logic, data, and tools.

---

# Basic Project Structure

The project structure must be close to the following:

```text
project_root/
│
├── main.py
│
├── app/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── constants.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── exceptions.py
│   │   ├── logging_config.py
│   │   └── utilities.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   ├── migrations/
│   │   └── repositories/
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── company.py
│   │   ├── contact.py
│   │   ├── email.py
│   │   └── lead.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── lead_service.py
│   │   ├── company_service.py
│   │   ├── contact_service.py
│   │   └── email_service.py
│   │
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── company_collector.py
│   │   ├── contact_collector.py
│   │   └── email_collector.py
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── company_parser.py
│   │   ├── contact_parser.py
│   │   └── email_parser.py
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── email_validator.py
│   │   ├── company_validator.py
│   │   └── lead_validator.py
│   │
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── csv_exporter.py
│   │   ├── excel_exporter.py
│   │   └── json_exporter.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── windows/
│   │   ├── pages/
│   │   ├── dialogs/
│   │   ├── widgets/
│   │   └── components/
│   │
│   └── resources/
│       ├── icons/
│       ├── images/
│       ├── styles/
│       └── translations/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── scripts/
│
├── data/
│   ├── exports/
│   ├── imports/
│   └── temporary/
│
├── logs/
│
├── docs/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── pyproject.toml
````

---

# 1. app/

This is the main folder containing the application code.

Most of the program code must be inside it.

Do not put random files in the project root if the file clearly belongs to one of the `app/` parts.

---

# 2. main.py (Project Root)

This is the program's entry point and lives at the project root, outside `app/`.

Its basic responsibility:

* Running the application.
* Initializing settings.
* Initializing core services.
* Initializing the database.
* Starting the main interface.

`main.py` must not contain the main business logic.

Example of allowed responsibilities:

```python
def main():
    initialize_application()
    initialize_database()
    start_application()
```

Do not put in it:

* Lead extraction operations.
* Long SQL queries.
* Web page parsing.
* Email verification.
* Lead filtering logic.

---

# 3. app/config/

Contains program settings and constants.

## settings.py

Contains:

* Database settings.
* Application settings.
* Path settings.
* External services settings.
* Lead extraction settings.
* Task settings.

Must not put sensitive secrets directly inside the code.

Use environment variables when needed.

## constants.py

Contains constant values used by the program.

Like:

* Lead types.
* Lead statuses.
* Data source types.
* Verification statuses.
* Supported file types.

---

# 4. app/core/

Contains core shared tools needed by more than one part of the application.

## exceptions.py

Contains project-specific custom exceptions.

Example:

```python
class LeadGenerationError(Exception):
    pass
```

Can create more specialized exceptions when needed.

## logging_config.py

Contains the `logging` system configuration.

## utilities.py

Contains small general tools that don't belong to a specific business domain.

Must not turn this file into a huge file containing everything.

If a certain function becomes related to a specific domain, it must be moved to the appropriate module.

---

# 5. app/database/

This folder is responsible for dealing with the database.

Contains:

* Database connection.
* Database setup.
* Migration operations.
* Repositories.

---

# 6. app/database/connection.py

Its responsibility:

* Creating the database connection.
* Managing the connection session.
* Providing a safe mechanism for database access.
* Closing the connection when needed.

Do not put business logic here.

---

# 7. app/database/repositories/

Contains the data access layer.

Each Repository is responsible for dealing with a specific type of data.

Examples:

```text
company_repository.py
contact_repository.py
email_repository.py
lead_repository.py
```

Repository Responsibilities:

* SELECT.
* INSERT.
* UPDATE.
* DELETE.
* Searching records.
* Saving records.
* Retrieving records.

Repository must not contain interface logic.

Nor must it contain data extraction logic from the internet.

---

# 8. app/models/

Contains the data models used in the program.

Examples:

```text
company.py
contact.py
email.py
lead.py
```

## Company

Represents the company.

Potential information:

* Name.
* Website.
* City.
* State.
* Country.
* Domain.
* Website URL.
* Source.

## Contact

Represents a contact person within the company.

Like:

* Name.
* Job title.
* Company.
* LinkedIn when needed.
* Data source.

## Email

Represents an email address.

Can contain:

* Email.
* Email type.
* Source.
* Verification status.
* Confidence score.

## Lead

Represents the final potential customer resulting from the collection and refinement process.

---

# 9. app/services/

Contains business logic.

This layer is responsible for coordinating operations between:

```text
UI
↓
Services
↓
Repositories / Collectors / Validators
```

Examples:

```text
lead_service.py
company_service.py
contact_service.py
email_service.py
```

## lead_service.py

Responsible for Lead-related operations.

Like:

* Creating a Lead.
* Updating a Lead.
* Filtering Leads.
* Processing a Lead.
* Merging company, contact, and email data.
* Applying project rules.

Most business rules must be in this layer or in specialized units linked to it.

---

# 10. app/collectors/

Contains code responsible for collecting data from external sources.

Examples:

```text
company_collector.py
contact_collector.py
email_collector.py
```

This layer can deal with:

* Web pages.
* Search engines.
* Public sources.
* APIs.
* Import files.
* External data sources.

Collector is responsible for **collecting data** only.

Must not turn Collector into a place for storing data or managing the user interface.

---

# 11. app/parsers/

Contains code for analyzing and converting raw data into structured data.

Example:

```text
company_parser.py
contact_parser.py
email_parser.py
```

If the program gets HTML or raw text, the Parser analyzes it and extracts the required data.

Typical sequence:

```text
Collector
    ↓
Raw Data
    ↓
Parser
    ↓
Structured Data
    ↓
Validator
    ↓
Service
    ↓
Repository
```

---

# 12. app/validators/

Contains data validation rules.

Examples:

```text
email_validator.py
company_validator.py
lead_validator.py
```

Can verify:

* Email format validity.
* Required data.
* Duplicate data.
* Phone number format validity.
* Company name validity.
* Lead data completeness.

Validator is responsible for **verification** not storage.

---

# 13. app/exporters/

Contains data export code.

Examples:

```text
csv_exporter.py
excel_exporter.py
json_exporter.py
```

Its responsibility:

* Taking structured data.
* Converting it to an appropriate format.
* Saving or exporting it.

Must not put lead extraction logic here.

---

# 14. app/ui/

This folder contains the graphical interface only.

The interface must be separated from business logic.

Structure:

```text
ui/
├── windows/
├── pages/
├── dialogs/
├── widgets/
└── components/
```

---

# 15. app/ui/windows/

Contains the main program windows.

Examples:

```text
main_window.py
settings_window.py
```

---

# 16. app/ui/pages/

Contains the main pages inside the program.

Example:

```text
dashboard_page.py
companies_page.py
contacts_page.py
leads_page.py
campaigns_page.py
sources_page.py
settings_page.py
```

Page is responsible for:

* Displaying data.
* Receiving user input.
* Running operations through Services.

Do not put SQL inside the page.

Do not put lead extraction logic inside the page.

---

# 17. app/ui/dialogs/

Contains small dialog windows.

Like:

```text
add_company_dialog.py
edit_lead_dialog.py
import_dialog.py
export_dialog.py
confirmation_dialog.py
```

---

# 18. app/ui/widgets/

Contains reusable Widgets.

Like:

```text
lead_table.py
company_card.py
search_bar.py
filter_panel.py
status_badge.py
```

If a UI element will be used in more than one place, prefer putting it here instead of duplicating code.

---

# 19. app/ui/components/

Contains larger or more complex UI components than a regular Widget.

Like:

```text
lead_filters.py
lead_details_panel.py
collection_controls.py
```

---

# 20. app/resources/

Contains non-code application resources.

Like:

```text
resources/
├── icons/
├── images/
├── styles/
└── translations/
```

## icons/

Program icons.

## images/

Images used in the interface.

## styles/

CSS/QSS files or style files used in the interface.

## translations/

Translation files if the program is multilingual.

---

# 21. tests/

Contains project tests.

Structure:

```text
tests/
├── unit/
├── integration/
└── fixtures/
```

## unit/

Unit tests in isolation.

Example:

```text
test_email_validator.py
test_lead_service.py
test_company_parser.py
```

## integration/

Tests for interaction between more than one layer.

Like:

```text
Service + Repository + Database
```

## fixtures/

Shared test data.

---

# 22. scripts/

Contains helper scripts that are not considered a direct part of the application logic.

Like:

* Development environment setup.
* Test data generation.
* Maintenance tools.
* Data conversion tools.
* Project management tools.

Do not use `scripts/` to hide business logic that should be inside `app/`.

---

# 23. data/

Contains local data created by the program or used during runtime.

Structure:

```text
data/
├── exports/
├── imports/
└── temporary/
```

## exports/

Files exported by the user.

## imports/

Files being imported.

## temporary/

Temporary data that is not considered a permanent part of the project.

Do not put secret data or passwords here.

---

# 24. logs/

Contains Log files resulting from running the application.

Must not contain Python code.

---

# 25. docs/

Contains project documentation.

Like:

```text
docs/
├── architecture/
├── database/
├── user-guide/
└── development/
```

---

# File Placement Rules

When creating a new file, the agent must ask the following question:

> What is the primary responsibility of this file?

Then place it in the folder that represents that responsibility.

Examples:

| Code Type | Location |
| --------- | -------- |
| Running the program | `main.py` (project root) |
| Program settings | `app/config/` |
| Project constants | `app/config/constants.py` |
| Custom exceptions | `app/core/exceptions.py` |
| Database connection | `app/database/` |
| SQL and data access | `app/database/repositories/` |
| Data models | `app/models/` |
| Business logic | `app/services/` |
| Data collection | `app/collectors/` |
| Raw data analysis | `app/parsers/` |
| Data validation | `app/validators/` |
| Data export | `app/exporters/` |
| Windows | `app/ui/windows/` |
| Pages | `app/ui/pages/` |
| Dialogs | `app/ui/dialogs/` |
| Widgets | `app/ui/widgets/` |
| UI components | `app/ui/components/` |
| Images and icons | `app/resources/` |
| Tests | `tests/` |
| Helper Scripts | `scripts/` |
| Imported files | `data/imports/` |
| Exported files | `data/exports/` |
| Temporary files | `data/temporary/` |
| Logs | `logs/` |
| Documentation | `docs/` |

---

# Layer Separation Rule

Must maintain the following separation:

```text
UI
  ↓
Services
  ↓
Collectors / Parsers / Validators / Repositories
  ↓
Database / External Sources
```

And must avoid the following paths:

```text
UI → Database directly
UI → SQL directly
UI → Collector directly
UI → HTTP requests directly
UI → Parser directly
```

Instead:

```text
UI
  ↓
Service
  ↓
Repository / Collector
```

---

# No Responsibility Duplication Rule

Do not create a new file if the responsibility clearly belongs to an existing file.

Before creating a new file:

1. Search for the file responsible for the same domain.
2. Check if the function can be added to it without making it huge.
3. If the function is an independent responsibility, create a specialized file.
4. Do not create small files without need.

---

# Large Files Rule

If a file comes to contain multiple responsibilities or becomes difficult to understand, must consider splitting it.

Bad example:

```text
lead_service.py
```

Containing:

* Lead collection.
* HTML analysis.
* Email verification.
* SQL.
* Export to Excel.
* Interface logic.

This is not acceptable.

Prefer:

```text
collectors/
parsers/
validators/
services/
database/repositories/
exporters/
ui/
```

So that each part has a clear responsibility.

---

# Folder Creation Rule

Do not create folders or future files without an actual need.

The structure must be:

* Clear.
* Simple.
* Extensible.
* Free of unnecessary complexity.

If there's no real need for a certain folder, do not add it just to follow the structure.

---

# Existing Project Modification Rule

When working on an existing project:

1. Inspect the current structure first.
2. Do not rebuild the entire project without reason.
3. Respect the current structure if it's logical.
4. If there's a clear deviation from this skill, fix it gradually.
5. Do not move files randomly.
6. Ensure all Imports are updated after moving files.
7. Run tests after structural changes.

---

# Imports Rule

Must use clear and organized Imports.

Avoid:

```python
from app import *
```

And avoid Circular Imports.

If splitting files leads to Circular Import, must redesign dependencies instead of using temporary solutions that hide the problem.

---

# Resources Rule

Do not put images, icons, or style files inside Python files.

Bad:

```text
app/ui/main_window.py
app/ui/logo.png
```

If resources are shared or part of application resources, prefer:

```text
app/resources/images/logo.png
```

---

# Database Rule

Do not put SQL files or database queries inside:

```text
ui/
collectors/
parsers/
```

Database access operations must be inside:

```text
app/database/
```

Especially:

```text
app/database/repositories/
```

---

# Business Logic Rule

Do not put Business Logic inside:

```text
ui/
models/
database/connection.py
```

Business logic must be in:

```text
app/services/
```

Or in specialized units linked to the business layer when necessary.

---

# Collector Rule

Collector is responsible for obtaining data from an external source.

Collector must not:

* Display an interface.
* Execute SQL directly.
* Save data to the database directly if that's the responsibility of Service/Repository.
* Contain Excel export logic.

---

# Parser Rule

Parser is responsible for converting raw data into structured data.

Example:

```text
HTML
  ↓
Parser
  ↓
Company / Contact / Email
```

Parser must not be responsible for:

* Database.
* Interface.
* Export.
* User management.

---

# Validator Rule

Validator is responsible for verification only.

Example:

```text
Raw Email
  ↓
Email Validator
  ↓
Valid / Invalid
```

Validator must not manage the interface or save data to the database.

---

# Exporter Rule

Exporter receives structured data and converts it to an exportable format.

Example:

```text
Lead Data
  ↓
CSV Exporter
  ↓
CSV File
```

And must not contain lead collection logic.

---

# UI Rule

The interface is responsible for:

* Displaying information.
* Receiving user input.
* Running operations.
* Displaying success and failure states.

The interface is NOT responsible for:

* SQL.
* HTTP requests.
* Scraping.
* Data analysis.
* Complex business rules.

---

# Database and Interface Rule

Preferred path:

```text
User
  ↓
UI
  ↓
Service
  ↓
Repository
  ↓
Database
```

And for data collection parts:

```text
User
  ↓
UI
  ↓
Service
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
  ↓
Database
```

---

# Reusability Rule

If a Function or Component is used in more than one place:

* Do not duplicate the code.
* Move the function to an appropriate layer.
* Use a shared Component, Utility, or Service depending on the function's nature.

Example:

If multiple pages need to search for Leads, do not create search logic inside each page.

Put the logic in:

```text
app/services/lead_service.py
```

And have the pages call it.

---

# Rule Before Creating Any File

Before creating any new file, the agent must determine:

1. What is the file's responsibility?
2. What layer does this responsibility belong to?
3. Does an existing file perform the same responsibility?
4. Will creating the file lead to duplication?
5. What files will depend on it?
6. Will it lead to Circular Import?
7. Does its location comply with Project Structure?

If the answer is unclear, must inspect the project structure first before creating any file or folder.

---

# Fundamental Rule for the Agent

Do not create files based on where the problem appears only.

Create the file according to the **architectural responsibility of the code**.

Example:

If a problem appears in the "Collect Leads" button inside the interface, this doesn't mean the lead collection logic should be placed inside the button file.

Correct:

```text
Button
  ↓
UI Handler
  ↓
Lead Service
  ↓
Collector
  ↓
Parser
  ↓
Validator
  ↓
Repository
```

---

# Final Principle

Every file must have a clear reason for its existence.

Every folder must represent a clear layer or responsibility.

It must be easy for any developer or AI agent to answer the question:

> Where do I put this code?

And the answer must depend on **the code's responsibility**, not just the feature name.

When in doubt, inspect the current project structure and existing files before creating any new file or folder.
