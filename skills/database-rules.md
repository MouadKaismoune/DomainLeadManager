---
name: database-rules
description: Defines rules for SQLite database management including relationships, normalization, duplicate prevention, and data integrity without rewriting the entire SQL schema.
---

# Database Rules Skill

## Purpose

This skill defines rules for working with SQLite database in the Lead Generation Application.

Codex must adhere to these rules when:

- Creating tables.
- Modifying tables.
- Adding columns.
- Creating relationships.
- Writing queries.
- Creating or modifying Repositories.
- Saving leads, companies, contacts, and emails.
- Handling duplicate data.
- Executing import operations.
- Executing update and delete operations.
- Designing or modifying database structure.

This skill does not contain a complete SQL Schema.

Codex must not rewrite the entire database just to make a small modification.

---

# 1. SQLite Fundamental Rule

The project uses SQLite as a local database.

Must treat SQLite as a true relational database, not just a file for storing data.

Must pay attention to:

- Primary Keys.
- Foreign Keys.
- Unique Constraints.
- NOT NULL.
- CHECK Constraints when needed.
- Indexes.
- Transactions.
- Referential Integrity.

---

# 2. Don't Rewrite SQL Entirely

When modifying the database, do not recreate all tables or rewrite the entire Schema if not necessary.

If the requirement is, for example:

> Add a column to the companies table

Then execute a small, targeted modification.

Do not rewrite:

- All tables.
- All relationships.
- All INSERT statements.
- All project data.

Unless there's a real technical reason requiring a comprehensive Migration.

---

# 3. Inspect Current Schema First

Before making any database modification, Codex must:

1. Inspect current Schema.
2. Know existing tables.
3. Know current columns.
4. Know Primary Keys.
5. Know Foreign Keys.
6. Know Unique Constraints.
7. Know Indexes.
8. Know existing relationships.
9. Know existing data if modification may affect it.

Do not assume current Schema matches what you expect.

---

# 4. Primary Key

Every table representing an independent entity must have a clear Primary Key.

Prefer using a fixed, unique identifier for each record.

Conceptual example:

```text
companies
    id

contacts
    id

emails
    id

leads
    id
```

Must not use company name or email itself as Primary Key.

Reason:

* Name may change.
* Email may change.
* Text values are not always suitable as internal identifiers.
* Relationships become more difficult.

---

# 5. Foreign Keys

When a record depends on another record, must use Foreign Key instead of storing the relationship as duplicate text.

Example:

```text
company
    id
      ↑
      │
contact
    company_id
```

Instead of:

```text
contact
    company_name
```

If the company already exists in the `companies` table.

---

# 6. Relationships

Must define relationship type before creating any new column.

Basic relationships:

## One-to-One

One entity links to only one record of another entity.

Do not use this type unless the relationship is actually 1:1.

## One-to-Many

One entity can link to multiple records.

Example:

```text
Company
   │
   ├── Contact
   ├── Contact
   └── Contact
```

Foreign key is usually on the many side:

```text
contacts.company_id
```

## Many-to-Many

When each side can link to multiple records of the other side.

Must use a junction table.

Example:

```text
companies
    │
    └── company_contacts ── contacts
```

Do not store multiple IDs inside a single column like:

```text
contact_ids = "1,4,7,12"
```

This is incorrect design for a relational database.

---

# 7. Don't Store Multiple Values in One Column

Do not put a group of values inside a single column.

Bad:

```text
emails = "info@example.com,sales@example.com,admin@example.com"
```

Correct is to have an independent table:

```text
emails
```

And link records to the company or contact using Foreign Key.

---

# 8. Normalization

Must design the database according to appropriate normalization principles.

Goal of Normalization is:

* Reduce duplication.
* Prevent data contradictions.
* Facilitate updates.
* Maintain correct relationships.
* Prevent storing same information in multiple places unnecessarily.

---

# 9. First Normal Form - 1NF

Values must be Atomic.

Meaning each cell contains a single logical value.

Bad:

```text
phone = "0550...,0660...,0770..."
```

Or:

```text
emails = "a@example.com,b@example.com"
```

Prefer storing each value in an appropriate record.

---

# 10. Second Normal Form - 2NF

Columns must depend on the appropriate primary key.

If a table contains data that doesn't depend on the entity the table represents, must reconsider the design.

Do not put repeated company information in every Contact record.

Bad example:

```text
contacts

id
contact_name
company_name
company_city
company_website
company_phone
```

If this information belongs to the company itself, it must be in the company table.

---

# 11. Third Normal Form - 3NF

Must avoid unnecessary indirect dependencies.

If a value can be derived from another entity, do not repeat it without reason.

Example:

```text
contacts
    company_id
    company_name
```

If `company_name` exists in `companies`, no need to repeat it in `contacts` unless there's a clear, intentional architectural reason.

---

# 12. Prevent Company Data Duplication

Company must represent a single logical entity.

Do not create a new company record every time you find a new Contact for the same company.

Wrong example:

```text
Company A + Contact 1
Company A + Contact 2
Company A + Contact 3
```

As separate company records.

Correct:

```text
companies
    Company A

contacts
    Contact 1 → Company A
    Contact 2 → Company A
    Contact 3 → Company A
```

---

# 13. Prevent Contact Duplication

Before creating a new Contact, must attempt to determine if the person already exists.

Do not always rely on name alone.

Can use a set of data when needed like:

```text
name
company
email
source
```

But matching rules must be clear and not lead to accidentally merging two different people.

---

# 14. Prevent Email Duplication

Email is often a duplication-sensitive value.

Before inserting a new Email:

1. Normalize the email.
2. Remove unnecessary spaces.
3. Unify case when needed.
4. Search for existing email.
5. Do not create a duplicate record if the email represents the same logical value.

Example:

```text
 SALES@Example.com
sales@example.com
```

May represent the same email after normalization.

But must not apply risky transformation rules to email without reason.

---

# 15. UNIQUE Constraints

When a certain value must be unique at the database level, prefer enforcing it using `UNIQUE`.

Do not rely only on:

```text
SELECT
Then
INSERT
```

Because two concurrent operations or different code paths may lead to Duplicates.

Rule:

> If the database itself knows a value must be unique, it's better for the database to enforce it.

---

# 16. Database-Level Integrity

Must not rely on Python alone to protect data integrity.

Python Validation is important, but must use database constraints when appropriate.

Examples:

* UNIQUE.
* NOT NULL.
* FOREIGN KEY.
* CHECK.

Can have two layers:

```text
Application Validation
        ↓
Database Constraints
```

---

# 17. Foreign Key Integrity

Must maintain correctness of relationships between tables.

Must not allow records pointing to a non-existent Parent.

Example:

```text
contacts.company_id
```

Must point to an existing company.

Must enable Foreign Key enforcement in SQLite when creating the connection.

---

# 18. Deleting Related Data

Before determining delete behavior, must think about relationships.

If a Company is deleted, what happens to:

* Contacts?
* Emails?
* Leads?
* Activities?

Do not use `CASCADE` randomly.

Must choose delete behavior based on project's Business Rules.

Possible options include:

```text
CASCADE
RESTRICT
SET NULL
```

And must choose them based on the meaning of the relationship.

---

# 19. Soft Delete

If data is historically important, do not actually delete it without reason.

Can use Soft Delete when the system needs to retain the record.

For example:

```text
is_deleted
deleted_at
```

But do not add Soft Delete to every table automatically.

Use it only when there's an actual need.

---

# 20. Timestamps

When needing to track records, use clear fields like:

```text
created_at
updated_at
```

Do not add timestamps to every table automatically.

Their presence must be related to the program's need to know creation or modification dates.

---

# 21. NULL

Must use `NULL` when the value means:

> No known value or not available.

Do not use dummy values like:

```text
""
"N/A"
"unknown"
"none"
"0"
```

As an alternative to NULL if NULL's meaning is most appropriate.

But must determine this based on the field's meaning.

---

# 22. Duplicates

Handling Duplicates must be part of system design, not just post-problem processing.

When collecting data from multiple sources, it's natural for the same company or same email to appear more than once.

Must have a clear strategy:

```text
Collect
   ↓
Normalize
   ↓
Identify
   ↓
Deduplicate
   ↓
Validate
   ↓
Store
```

---

# 23. Normalize Before Deduplication

Do not compare raw data directly if it may contain formal differences.

Example:

```text
Example Company
example company
EXAMPLE COMPANY
Example  Company
```

May be the same company.

Must use appropriate normalization before comparison.

But must not assume textual similarity always means entities are identical.

---

# 24. Exact Duplicate vs Possible Duplicate

Must distinguish between:

## Exact Duplicate

Clearly identical data.

Can be prevented using:

* UNIQUE.
* Clear Matching.
* Normalization.

## Possible Duplicate

Similar data but not confirmed.

Example:

```text
ABC Solutions
ABC Solution
```

Do not merge automatically just because of similarity.

Must use stronger rules or leave for review.

---

# 25. Deduplication Doesn't Mean Random Data Deletion

When discovering Duplicate:

Do not delete one of the two records directly.

Must first know:

* Which record is the primary?
* Does one contain additional information?
* Are there relationships linked to either?
* Are there different Sources?
* Should data be merged?
* Should source record be retained?

---

# 26. Source Tracking

Since the program collects Leads from multiple sources, must think about data source.

Source may be:

* Website.
* Search Engine.
* Directory.
* Import File.
* API.
* Manual Entry.

Do not lose source information when merging data.

If a company exists from two different sources, this doesn't necessarily mean creating two companies.

Can retain a relationship or record of sources per design.

---

# 27. Don't Duplicate Derived Information

Do not store the same information in multiple tables just for easy access.

Example:

If:

```text
lead.company_id
```

Points to the company, no need to repeat:

```text
lead.company_name
lead.company_city
lead.company_website
```

Unless there's a clear reason like:

* Historical Snapshot.
* Intentional Cache.
* Studied Denormalization.
* Real Performance Requirements.

Any Denormalization must be a conscious decision, not a result of programming convenience.

---

# 28. Denormalization

Can use Denormalization when there's a real need, such as:

* Improving performance of specific queries.
* Retaining a historical snapshot.
* Reducing Join operations in a studied scenario.

But do not use Denormalization just because SQL became more complex.

If duplicate data is intentionally added, must document the reason for its existence and the Source of Truth.

---

# 29. Source of Truth

Every important piece of information must have a clear location for its master copy.

Example:

```text
Company Name
```

Must have a clear primary source.

If the name exists in:

```text
companies.name
leads.company_name
contacts.company_name
```

It becomes difficult to know which value is correct.

Therefore must avoid this design unless the duplication is intentional and documented.

---

# 30. Indexes

Must create Indexes on columns frequently used in:

* Search.
* JOIN.
* Filtering.
* Sorting.
* Duplicate verification.

Potential examples:

```text
email
company_id
contact_id
domain
created_at
```

But do not create an Index for every column.

Unnecessary additional Indexes can:

* Increase database size.
* Slow down write operations.
* Increase system complexity.

---

# 31. Search Fields

If the program frequently searches for:

```text
company name
domain
email
phone
```

Must evaluate the need for an appropriate Index.

Do not try to solve search problems only by duplicating data in other tables.

---

# 32. Transactions

Operations consisting of multiple related changes must be executed within an appropriate Transaction.

Example:

```text
Create Company
    +
Create Contact
    +
Create Email
```

If the last part fails, must not leave data in an inconsistent state.

Rule:

> Operations that must succeed as one unit must be executed as one unit.

---

# 33. Commit

Do not use Commit randomly after every small operation if multiple operations form a single logical operation.

Prefer letting an appropriate layer control Transaction boundaries.

---

# 34. Parameterized Queries

Must use Parameterized Queries.

Do not construct SQL using string concatenation to insert user data.

Bad:

```python
query = f"SELECT * FROM leads WHERE email = '{email}'"
```

Correct is to use parameters provided by the SQLite driver.

---

# 35. Repository Pattern

Repository layer must handle the database.

Preferred path:

```text
UI
  ↓
Service
  ↓
Repository
  ↓
SQLite
```

And UI pages must not contain direct SQL.

---

# 36. Business Logic Is Not in Database Layer

Repository is responsible for data access.

Do not put complex Business Logic inside it like:

* Determining Lead quality.
* Choosing the best Contact.
* Calculating Lead Score.
* Making marketing decisions.
* Customer processing rules.

These are responsibilities of the Service layer or appropriate business layers.

---

# 37. Database Schema Changes

When modifying Schema:

1. Inspect current structure.
2. Determine required change.
3. Verify current data.
4. Determine change impact on relationships.
5. Create small Migration if project uses Migrations.
6. Preserve existing data.
7. Test the application after modification.

Do not use destructive solutions like deleting the database and recreating it during development unless intentionally clear.

---

# 38. Migration Safety

Any Migration must be:

* Clear.
* Traceable.
* Specific in purpose.
* As safe as possible.
* Compatible with existing data.

If the change may lead to data loss, must handle it with extreme caution.

---

# 39. Don't Create New Table Just to Solve a UI Problem

If a specific page needs to display some information, this doesn't automatically mean creating a new table.

Ask first:

1. Does the information already exist?
2. Can it be obtained via JOIN?
3. Is it truly an independent Entity?
4. Does it have an independent lifecycle?
5. Does it have its own relationships?

Create a new table only if there's a logical need.

---

# 40. Don't Merge Different Entities

Do not put different entities in one table just to reduce the number of tables.

Example:

```text
companies
contacts
emails
```

Are not necessarily the same entity.

Must separate them when each has:

* Independent identity.
* Different properties.
* Different relationships.
* Different lifecycle.

---

# 41. Lead as an Entity

Must clearly define the meaning of `Lead` before designing the relationship.

If Lead represents a business opportunity linked to a Company or Contact, must use appropriate Foreign Keys instead of copying all Company and Contact data inside Lead.

Conceptual example:

```text
Lead
  ├── company_id
  ├── contact_id
  └── ...
```

But the final relationship must follow the project's Business Domain.

---

# 42. Company and Domain

If the program deals with Domains, must determine whether a Domain is:

* Just a field inside Company.
* Or an independent Entity.

If a company has only one Domain and project rules are simple, it may be a field in Company.

If a company can own multiple Domains or if a Domain has independent data and relationships, it's better to think of a separate Entity.

Do not automatically create a Domains table without need.

---

# 43. Email as an Independent Entity

If the program needs to store:

* More than one Email.
* Verification status.
* Email source.
* Email type.
* Date found.
* Relationship with Contact or Company.

Then Email may be an independent Entity.

Must determine the relationship before putting the email in another table.

---

# 44. Don't Use JSON as a Substitute for Relationships

Do not use JSON or TEXT to store relational data just to avoid creating a table.

Bad:

```text
contacts = '[{"name":"John"},{"name":"Sarah"}]'
```

If Contacts are real entities that need searching, filtering, and relationships.

Use appropriate SQLite tables and relationships.

JSON can be used when data is truly semi-structured and doesn't need to be handled as relational entities.

---

# 45. SQLite Limitations

Must take SQLite characteristics into account.

Do not assume SQLite works exactly like MySQL or PostgreSQL.

When using advanced features, must verify compatibility with SQLite and its version.

Especially when dealing with:

* ALTER TABLE.
* Constraints.
* Concurrency.
* Transactions.
* Indexes.
* Foreign Keys.

---

# 46. Concurrency

SQLite is very suitable for a local Desktop application, but must pay attention to concurrent write operations.

Do not assume the same concurrency model as server databases.

Must avoid unnecessarily long write operations.

---

# 47. Connection Management

SQLite connection creation and management must be in the database layer.

Do not create a new random connection inside every UI component.

Upper components must not know details of:

```text
sqlite3.connect(...)
```

And must use the appropriate database layer.

---

# 48. Backup

Do not treat the SQLite file as a normal file during write operations.

When executing Backup, must use a safe and appropriate mechanism for the database state.

Must not copy the database in a way that could produce an inconsistent copy during write operations.

---

# 49. Error Handling

Database errors must not reach the user directly in their raw technical form.

Preferred path:

```text
SQLite Error
    ↓
Repository
    ↓
Service
    ↓
Application Error
    ↓
UI
    ↓
User-friendly Message
```

Must log technical details in Logs when needed.

---

# 50. Minimal Change Rule

When modifying the database:

> Change the minimum amount of Schema necessary to achieve the required result.

Do not redesign existing tables unless there's a real design problem.

---

# 51. Duplicate Check Rule Before Adding a Table

If a need arises to store new information, ask:

1. Is there a table representing this information?
2. Can it be linked to an existing table?
3. Is the information duplicated elsewhere?
4. Will creating a new table lead to Duplicate Data?
5. Is this information truly an independent Entity?

---

# 52. Duplicate Check Rule Before Adding a Column

Before adding a column:

1. Search for the same information in other tables.
2. Determine Source of Truth.
3. Check possibility of using Foreign Key or JOIN.
4. Do not add the column if it will duplicate existing information without a clear reason.

---

# 53. Don't Over-Normalize Rule

Normalization is important, but must not convert every value into an independent table without reason.

Example:

Not every:

```text
country
city
source
status
```

Necessarily needs an independent table.

Must choose design based on:

* Nature of data.
* Relationships.
* Changeability.
* Need for Metadata.
* Search requirements.
* Business Rules.

---

# 54. Balance Rule

Good design must balance:

```text
Data Integrity
+
Normalization
+
Performance
+
Simplicity
+
Maintainability
```

Do not choose an overly complex design just because it's more normalized.

Do not choose a disorganized design just because it's easier initially.

---

# 55. Checklist Before Modifying Database

Before executing any change, Codex must verify:

* [ ] Did I understand the current Schema?
* [ ] Is the change necessary?
* [ ] Is there a table or column serving the same purpose?
* [ ] Will the change lead to Duplicate Data?
* [ ] Is there a relationship between entities?
* [ ] Should Foreign Key be used?
* [ ] Should UNIQUE be used?
* [ ] Should an Index be used?
* [ ] Can the change affect existing data?
* [ ] Does the change need a Transaction?
* [ ] Does it need a Migration?
* [ ] Is it compatible with SQLite?
* [ ] Will it affect the Repository?
* [ ] Will it affect Services?
* [ ] Will it affect the UI?
* [ ] Are there tests that need updating?

---

# Final Principle

The database must be:

```text
Relational
Normalized
Consistent
Traceable
Maintainable
Safe from unnecessary duplicates
```

And Codex must think about the database from the perspective of **entities, relationships, and source of truth**, not just from the perspective of creating columns and tables.

When adding any new part to the system:

```text
Identify Entity
      ↓
Define Relationship
      ↓
Check Existing Data
      ↓
Check Normalization
      ↓
Check Duplicates
      ↓
Define Constraints
      ↓
Define Indexes if needed
      ↓
Implement Minimal Change
      ↓
Test Data Integrity

Most important rule:

> Do not add duplicate data, a new relationship, or a new table before verifying that the current structure doesn't already provide the correct place for this information.
