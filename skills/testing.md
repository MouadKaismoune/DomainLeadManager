---
name: testing
description: Defines testing rules for the project focusing on Services, Repositories, database, Business Logic, and data collection/import/export operations, guiding the agent to write actually useful tests rather than ceremonial ones.
---

# Testing

## 1. Purpose

This skill defines project testing rules and ensures the code works correctly without breaking existing parts.

Tests must focus on:

* Business Logic.
* Services.
* Repositories.
* Database operations.
* Validators.
* Parsers.
* Collectors when needed.
* Import/Export.
* Duplicate Detection.
* Lead Management.
* Important and sensitive operations.

The goal is not to increase the number of tests, but to ensure that **important project behavior is protected by reliable tests**.

---

# 2. Fundamental Principle

Must test:

```text
Correct Behavior
+
Business Rules
+
Data Integrity
+
Error Handling
+
Important Edge Cases
```

Testing that a Function works in the ideal case only is not enough.

Must also test:

```text
Invalid Input
Empty Data
Missing Data
Duplicates
Database Errors
Unexpected Data
Boundary Cases
```

---

# 3. Testing Pyramid

Preferred project approach:

```text
         Integration Tests
               ▲
               │
         Service Tests
               ▲
               │
           Unit Tests
```

The most numerous tests should be Unit Tests.

Integration Tests are used to ensure multiple parts work together correctly.

---

# 4. Unit Tests

Unit Test tests a small, independent piece of code.

Examples:

```text
normalize_domain()
validate_email()
calculate_similarity()
validate_company()
detect_duplicate()
```

Unit Tests must be:

* Fast.
* Independent.
* Repeatable.
* Not dependent on Internet.
* Not dependent on a real Database when not needed.

---

# 5. Service Tests

Must test Services because they contain Business Logic.

Examples:

```text
CompanyService
LeadService
ContactService
EmailService
```

Must test:

```text
Create
Read
Update
Business Rules
Validation
Duplicate Detection
Status Changes
Error Handling
```

---

# 6. Repository Tests

Must test Repositories to ensure Database operations work as expected.

Test:

```text
Insert
Select
Update
Delete
Search
Filtering
Relationships
Constraints
Transactions
```

Must use a separate Test Database.

Do not use the user's real Database during tests.

---

# 7. Database Tests

Test the integrity of relationships and constraints.

Like:

```text
Primary Keys
Foreign Keys
Unique Constraints
NOT NULL
CHECK Constraints
Indexes where relevant
Transactions
```

Must ensure the Database prevents the incorrect states it's supposed to prevent.

---

# 8. Test Database

Tests must be isolated from real application data.

Can use:

```text
Temporary SQLite Database
```

Or a Database dedicated to tests.

Tests must not:

```text
Modify User Data
Delete Real Data
Create Test Records in Production Database
```

---

# 9. Test Isolation

Each Test must be as independent as possible.

Do not rely on a previous Test creating data.

Bad:

```text
test_create_company()
        ↓
test_update_company()
        ↓
test_delete_company()
```

If the second Test needs the first one's data, it becomes non-independent.

Prefer each Test creating the data it needs.

---

# 10. Setup and Teardown

Use Fixtures or appropriate Setup/Teardown to create and clean up test data.

Example:

```text
Create Test Database
        ↓
Create Schema
        ↓
Insert Test Data
        ↓
Run Test
        ↓
Cleanup
```

Do not leave test data affecting other Tests.

---

# 11. Fixtures

Use Fixtures for repeated and important data.

Examples:

```text
sample_company
sample_domain
sample_contact
sample_email
sample_lead
```

But do not make Fixtures huge or complex in a way that makes tests hard to understand.

---

# 12. Test Naming

Test names must clarify:

```text
What
When
Expected Result
```

Example:

```python
def test_normalize_domain_removes_protocol():
    ...
```

Or:

```python
def test_create_company_rejects_empty_name():
    ...
```

Or:

```python
def test_duplicate_detection_identifies_same_domain():
    ...
```

Avoid:

```python
def test_company():
    ...
```

---

# 13. Arrange / Act / Assert

Prefer organizing tests like this:

```text
Arrange
→ Act
→ Assert
```

Example:

```python
def test_create_company():
    # Arrange
    company = Company(name="Example")

    # Act
    result = service.create_company(company)

    # Assert
    assert result.name == "Example"
```

This makes the test easy to read.

---

# 14. Test One Behavior

Prefer one Test testing one clear Behavior.

Instead of a huge Test testing:

```text
Create
Update
Delete
Search
Export
```

Use separate Tests.

---

# 15. Avoid Overly Broad Tests

Do not make a single Test responsible for dozens of different cases if that makes the failure reason unclear.

Small, clear tests are easier to:

```text
Debugging
Maintenance
Refactoring
```

---

# 16. Testing Business Rules

Business Rules must be among the most important parts of tests.

Test the rules in `business-rules.md`.

Especially:

```text
Company can have multiple Domains
Personal Email belongs to one Person
No automatic merge
No automatic deletion
Duplicate Detection
Lead Statuses
Source Preservation
```

---

# 17. Company and Domain Relationship

Must test that:

```text
One Company
→ Multiple Domains
```

Example:

```text
Company A
├── domain-a.com
├── domain-b.com
└── domain-c.com
```

Adding a new Domain must not automatically create a new Company if Business Rules specify that multiple Domains can belong to the same Company.

---

# 18. Contact and Email Tests

Test that Personal Email is not linked to another person without evidence.

Must test cases:

```text
Same Email + Same Contact
Same Email + Different Contact
Different Email + Same Contact
Generic Company Email
Missing Email
Invalid Email
```

---

# 19. Generic Emails

Test handling of Emails like:

```text
info@example.com
sales@example.com
support@example.com
contact@example.com
```

Must not create a fake personal Contact from them.

---

# 20. Duplicate Detection Tests

Duplicate Detection is one of the most important parts to test.

Test:

```text
Confirmed Duplicate
Possible Duplicate
Not Duplicate
```

And test Signals like:

```text
Domain
Website
Company Name
Phone
Address
Location
Email
Contact Name
Company Relationship
```

---

# 21. No Automatic Delete Test

Must have a Test confirming that Duplicate Detection does not automatically lead to data deletion.

Example:

```text
Duplicate detected
        ↓
Record remains
        ↓
Duplicate status/review information created
```

Detection alone must not lead to:

```text
DELETE
```

---

# 22. No Automatic Merge Test

Must test that Possible Duplicate does not automatically lead to Merge.

Example:

```text
Possible Duplicate
        ↓
Flag for Review
```

Not:

```text
Possible Duplicate
        ↓
Automatic Merge
```

---

# 23. Lead Status Tests

Test all approved Lead Statuses (per the canonical list in `project-overview.md`):

```text
new
researching
ready
contacted
interested
not_interested
archived
```

Must test allowed and disallowed transitions per Business Rules.

---

# 24. Archived vs Deleted

Must test that:

```text
archived
```

Does not mean:

```text
Deleted
```

And:

```text
not_interested
```

Does not mean:

```text
Deleted
```

The Record must remain unless an explicit, allowed delete operation is executed.

---

# 25. Validation Tests

Must test Validators on correct and incorrect cases.

Email example:

```text
valid@example.com
invalid-email
missing@
@example.com
empty
None
```

Domain example:

```text
example.com
www.example.com
https://example.com
invalid domain
empty
```

---

# 26. Edge Cases

Do not test only normal cases.

Test:

```text
Empty String
Whitespace
None
Very Long String
Special Characters
Unicode
Arabic Text
French Characters
Duplicate Values
Large Dataset
Zero
Negative Values where invalid
Boundary Values
```

---

# 27. Arabic and Unicode

Because the project may handle Arabic, French, and English data, must test Unicode.

Example:

```text
شركة الجزائر
Café
Électricité
محمد
```

Must ensure that:

* Database saves the data.
* Search works.
* Export doesn't corrupt text.
* Import works.
* UI displays text correctly.

---

# 28. Normalization Tests

Any important Normalization Logic must be tested.

Like:

```text
Email Normalization
Domain Normalization
Phone Normalization
Company Name Normalization
```

Example:

```text
https://example.com
http://example.com
www.example.com
example.com
```

Must ensure Normalization gives the expected result per project rules.

---

# 29. Search Tests

Test Search and Filtering.

Like:

```text
Search by Company
Search by Domain
Search by Email
Filter by Lead Status
Filter by Source
Filter by Duplicate Status
```

Also test:

```text
No Results
Partial Match
Case Differences
Whitespace
Special Characters
```

---

# 30. Repository Relationship Tests

Test relationships between:

```text
Company
Domain
Contact
Email
Lead
```

Especially:

```text
Company → Domains
Company → Contacts
Contact → Emails
Company → Leads
```

Must ensure relationships don't lead to orphaned or incorrect data.

---

# 31. CRUD Tests

For important Entities, test:

```text
Create
Read
Update
Delete
```

But do not assume every Entity must have the same Delete behavior.

Some data may be:

```text
Archived
Soft Deleted
Protected
```

Per Business Rules.

---

# 32. Update Tests

Test that Update:

* Changes the required field.
* Does not erase other fields without reason.
* Does not change Relationships unintentionally.
* Preserves existing data.

Especially when incomplete data arrives.

---

# 33. Data Preservation Tests

Example:

Existing:

```text
website = "https://example.com"
phone = "0555000000"
```

Incoming:

```text
website = ""
phone = None
```

Must test that good existing data is not silently deleted or replaced.

---

# 34. Transaction Tests

Must test Transactions.

Example:

```text
Create Company
+
Create Domain
+
Create Lead
```

If the third operation fails, must ensure:

```text
Rollback
```

And that the Database doesn't contain partial incorrect data.

---

# 35. Rollback Test

Must have a Test that intentionally fails inside a Transaction and verifies that:

```text
Before Transaction
        ↓
Operation A
        ↓
Operation B fails
        ↓
Rollback
        ↓
Database returns to valid state
```

---

# 36. Error Handling Tests

Test `error-handling.md` rules.

Like:

```text
Database Error
File Error
Invalid Input
Network Error
Parsing Error
Permission Error
Unexpected Error
```

Must ensure the application:

* Does not hide the error.
* Logs the error when needed.
* Displays an appropriate message.
* Preserves data.

---

# 37. "No Data" vs "Error"

Must have Tests confirming the difference between:

```text
No Results
```

And:

```text
Database Failure
```

Example:

```text
Search → []
```

May mean:

```text
No matching records
```

While Database failure must produce a clear Error.

---

# 38. File Tests

Test:

```text
File Exists
File Missing
Invalid File
Empty File
Permission Error
Invalid Encoding
Large File
```

Especially Import and Export.

---

# 39. Import Tests

Test:

```text
Valid File
Invalid File
Missing Columns
Extra Columns
Empty Rows
Invalid Email
Duplicate Records
Large File
Unicode Data
Partial Errors
```

Must ensure invalid data is not accidentally saved.

---

# 40. Export Tests

Test:

```text
CSV Export
Excel Export
JSON Export
Empty Dataset
Large Dataset
Unicode Data
Invalid Destination
Permission Error
```

And ensure successful Export produces a valid file.

---

# 41. Parser Tests

Parser must be tested with:

```text
Valid
Empty
Malformed
Unexpected
Incomplete
Changed Structure
```

Especially if the Parser deals with Website or API data.

---

# 42. Collector Tests

Do not depend Unit Tests on the real Internet.

Prefer using:

```text
Mock
Fake
Stub
Fixture
```

To test the Collector.

Example:

```text
Fake Response
        ↓
Collector
        ↓
Expected Parsed Data
```

This makes tests:

* Faster.
* Stable.
* Repeatable.

---

# 43. Network Tests

Test cases like:

```text
200 Success
404
403
429
500
Timeout
Connection Failure
Invalid Response
```

Using Mock/Fake when possible.

---

# 44. Avoid Real External Services in Unit Tests

Do not make Unit Tests depend on:

```text
Internet
Real API
Real Website
External Search Engine
```

Except in dedicated Integration Tests.

The goal is for Unit Tests to work even without Internet.

---

# 45. Mocking

Use Mock when you need to isolate an external Dependency.

Like:

```text
Network Client
File System
External API
Time
Database
```

But do not use Mock for everything.

Mock must solve a real problem in the test.

---

# 46. Do Not Over-Mock

If a test contains dozens of Mocks, the test may be testing Implementation instead of Behavior.

Priority:

```text
Test Behavior
```

Not:

```text
Test Every Internal Method Call
```

---

# 47. Integration Tests

Integration Tests verify that multiple Components work together.

Examples:

```text
Service
+
Repository
+
SQLite
```

Or:

```text
Import
+
Parser
+
Validator
+
Service
+
Database
```

---

# 48. Integration Database Tests

Must use a real SQLite Test Database when testing:

```text
Repositories
Transactions
Foreign Keys
Constraints
Queries
Relationships
```

Because a Mock Database doesn't prove that real SQL works.

---

# 49. UI Tests

UI Tests are not the first priority.

Must focus first on:

```text
Business Logic
Services
Repositories
Database
Validation
Critical Workflows
```

Can test UI basically to ensure:

```text
Navigation
Form Validation
Important Actions
Error Display
Loading State
```

Per the Framework used.

---

# 50. Test Critical Workflows

Must test important operations end-to-end.

Like:

```text
Create Company
    ↓
Add Domain
    ↓
Add Contact
    ↓
Add Email
    ↓
Create Lead
```

And:

```text
Collect Data
    ↓
Parse
    ↓
Validate
    ↓
Detect Duplicate
    ↓
Save
```

---

# 51. Regression Tests

When fixing a Bug:

1. Create a Test that reproduces the problem.
2. Ensure the Test fails before the fix.
3. Fix the problem.
4. Ensure the Test passes.
5. Keep the test to prevent the problem from returning.

This is called a Regression Test.

---

# 52. Bug Fix Rule

Do not just fix a Bug without a Test when it's easy to create a Test for it.

Preferred flow:

```text
Bug
→ Reproduce
→ Write Test
→ Fix
→ Test Passes
```

---

# 53. Tests Before Refactoring

Before major Refactoring, must ensure there are enough Tests protecting current Behavior.

If Tests don't exist, add important Tests first when possible.

---

# 54. Test Coverage

Coverage is useful but not the end goal.

Do not try to reach:

```text
100%
```

At any cost.

The important thing is covering:

```text
Critical Business Logic
Critical Database Operations
Important Error Paths
Important Edge Cases
```

Testing 80% of the code usefully is better than 100% with ceremonial tests.

---

# 55. Tests Must Be Deterministic

The same Test must give the same result in the same conditions.

Avoid unnecessary dependence on:

```text
Current Time
Random Values
Internet
External Services
Machine-specific Paths
Environment State
```

If these things are necessary, must control them during the test.

---

# 56. Test Performance

Unit Tests must be as fast as possible.

If a Test becomes slow due to:

```text
Network
Large Database
File Operations
External Services
```

Try to isolate it or use Mock/Fixture in Unit Test.

---

# 57. Test Data

Test data must be:

* Clear.
* As small as possible.
* Representative of the case being tested.
* Not linked to real user data.

Avoid huge Test Data if not necessary.

---

# 58. No Production Data

Forbidden to use real user data inside Automated Tests unless authorized and properly anonymized.

Better to use Synthetic Test Data.

---

# 59. Testing File Paths

Do not rely on fixed paths like:

```text
/home/user/project/...
```

Use Temporary Directories or Paths created during the test.

---

# 60. Testing Configuration

Test that the program correctly handles:

```text
Missing Configuration
Invalid Configuration
Default Configuration
Environment Variables
Missing API Credentials
```

But do not put real Credentials inside Tests.

---

# 61. Test Failures

When a Test fails:

Do not change the test just to make it pass.

Must determine:

```text
Test Wrong?
Code Wrong?
Expected Behavior Changed?
Business Rule Changed?
```

Then modify the test or code based on the real reason.

---

# 62. Never Weaken Tests

Forbidden to change Assert just because the current code fails.

The Test must reflect the actually required behavior.

---

# 63. Tests and Business Changes

If a Business Rule changes intentionally, must update:

```text
Business Logic
+
Tests
+
Documentation/Skills
```

So they all reflect the new behavior.

---

# 64. Test Organization

Prefer organizing tests by type:

```text
tests/
├── unit/
│   ├── services/
│   ├── validators/
│   ├── parsers/
│   └── utilities/
├── integration/
│   ├── repositories/
│   ├── database/
│   └── workflows/
└── fixtures/
```

Maintain organization compatible with `project-structure.md`.

---

# 65. Naming Test Files

Use clear names.

Example:

```text
test_lead_service.py
test_company_service.py
test_company_repository.py
test_email_validator.py
test_domain_normalizer.py
```

---

# 66. Testing Checklist

Before considering a Feature task complete:

```text
[ ] Happy path tested
[ ] Invalid input tested
[ ] Edge cases tested
[ ] Business rules tested
[ ] Database behavior tested when relevant
[ ] Error handling tested
[ ] Transaction behavior tested when relevant
[ ] Duplicate behavior tested when relevant
[ ] Regression test added for fixed bugs
[ ] No real production data used
[ ] No real external service required for Unit Tests
```

---

# 67. AI Agent Testing Rules

When adding or modifying a Feature, the agent must:

1. Understand the requirement.
2. Identify affected Business Rules.
3. Identify affected Layers.
4. Search for existing Tests related to the Feature.
5. Modify existing Tests if needed.
6. Add new Tests for important cases.
7. Run appropriate tests.
8. Fix Regression if it appears.
9. Do not delete a Test just because it failed.
10. Do not consider a Feature complete if important Tests are failing.

---

# 68. Before Changing Existing Code

Before modifying existing Logic:

```text
Inspect Existing Tests
        ↓
Understand Expected Behavior
        ↓
Modify Code
        ↓
Run Related Tests
        ↓
Run Broader Test Suite
```

If no Tests exist, create Tests for important cases when possible.

---

# 69. After Database Changes

After modifying Database-related code:

Must test:

```text
Schema Compatibility
Queries
Relationships
Constraints
Insert
Update
Select
Transactions
```

And it's not enough to just verify the application opens without Error.

---

# 70. After Business Rule Changes

If a Business Rule changes:

Must review Tests covering:

```text
Services
Validation
Duplicate Detection
Lead Status
Relationships
```

And old Tests representing Behavior that's no longer correct must not remain.

---

# 71. After UI Changes

If the modification is UI-only and doesn't change Logic:

Test at least:

```text
Page opens
Action works
Validation works
Error displays correctly
Loading state works
Navigation remains functional
```

No need to re-test the entire project due to a simple visual change unless the change affects Logic.

---

# 72. Test Execution Strategy

For a small modification:

```text
Run related tests first
        ↓
Run broader tests if needed
```

For a large modification:

```text
Run Unit Tests
        ↓
Run Integration Tests
        ↓
Run Critical Workflow Tests
```

---

# 73. Final Testing Principle

Tests are not just to prove the code works.

Tests must protect the project from:

```text
Regression
+
Invalid Data
+
Broken Business Rules
+
Database Inconsistency
+
Unexpected Errors
```

Final goal:

```text
Change Code
    ↓
Run Tests
    ↓
Know What Still Works
    ↓
Know What Broke
    ↓
Fix Safely
```

---

# 74. Final Rules

The agent must always adhere to these rules:

```text
Test important behavior, not just code coverage.
Keep tests independent.
Keep unit tests fast.
Do not use production data.
Do not depend on the real Internet in unit tests.
Use a separate test database.
Test both success and failure.
Test business rules.
Test database constraints.
Test transactions and rollback.
Test duplicate detection.
Test important edge cases.
Preserve regression tests for fixed bugs.
Do not weaken tests to make them pass.
Do not delete failing tests without understanding why.
Update tests when business behavior intentionally changes.
Prefer testing behavior over implementation details.
```

Most important rule:

```text
A feature is not complete simply because the code runs.

A feature is complete when its important behavior is implemented,
tested, and protected against regression.
