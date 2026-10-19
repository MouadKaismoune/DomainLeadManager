---
name: ai-development-rules
description: Defines the development methodology for the AI agent, specifying how to understand requests, inspect projects, plan changes, and avoid unnecessary modifications.
---

# AI Development Rules

## 1. Purpose

This skill defines how the AI agent should work within the project.

The agent must not treat the project as a collection of files to be modified directly, but as an integrated system with:

* Architecture.
* Business Rules.
* Database Rules.
* Project Structure.
* Coding Rules.
* Error Handling.
* Testing Rules.
* Dependencies.
* Existing Behavior.

The goal is for the agent's modifications to follow:

```text
Understand
→ Inspect
→ Plan
→ Modify
→ Test
→ Verify
```

And NOT:

```text
Request
→ Guess
→ Edit Files
```

---

# 2. Fundamental Rule

Before writing or modifying any code:

```text
DO NOT GUESS.
INSPECT THE PROJECT FIRST.
```

The agent must understand:

* What is requested.
* Where the problem exists.
* What files are related.
* What Layer is affected.
* What Business Rules are associated.
* What tests exist.
* What potential impacts on the rest of the system.

---

# 3. Read Skills Before Working

The agent must refer to the Skills in the project before executing tasks affected by them.

Especially:

```text
project-overview.md
business-domain.md
architecture.md
project-structure.md
database-rules.md
business-rules.md
ui-guidelines.md
coding-rules.md
error-handling.md
testing.md
ai-development-rules.md
```

Do not assume the rules in these files are unimportant.

These files represent:

```text
Project Knowledge
+
Project Constraints
+
Development Rules
```

---

# 4. Don't Read Everything Unnecessarily

The agent does not need to re-read all files for every task if unnecessary.

Must identify the Skills relevant to the task.

Example:

Database modification:

```text
architecture.md
database-rules.md
business-rules.md
coding-rules.md
testing.md
```

UI modification:

```text
architecture.md
ui-guidelines.md
coding-rules.md
testing.md
```

Duplicate Detection modification:

```text
business-domain.md
business-rules.md
architecture.md
database-rules.md
testing.md
```

---

# 5. Rule Priority Order

When instructions conflict, follow this priority:

```text
1. System / Platform Constraints
2. Project Architecture
3. Business Rules
4. Database Rules
5. Security Requirements
6. Error Handling Rules
7. Testing Rules
8. Coding Rules
9. UI Guidelines
10. Personal Implementation Preference
```

Must not choose the easier solution if it violates Architecture or Business Rules.

---

# 6. Understand Request Before Modifying

Before executing any task, determine:

```text
What is requested?
What is the expected behavior?
What currently happens?
What should change?
What should NOT change?
```

If the request is clear, do not ask unnecessary questions.

If there is genuine ambiguity affecting Architecture, Business Logic, or Data Integrity, must request clarification instead of guessing.

---

# 7. Explore Project First

Before modifying a file, the agent must inspect the project to know:

```text
Project Structure
Relevant Files
Existing Classes
Existing Functions
Existing Services
Existing Repositories
Existing Tests
Existing Patterns
Dependencies
```

Do not create a new file if the project already contains a suitable file for the required responsibility.

---

# 8. Search Before Creating

Before creating:

```text
Class
Function
Service
Repository
Utility
Component
Validator
```

Must search for existing code that performs the same function.

Goal is to prevent:

```text
Duplicate Code
Duplicate Services
Duplicate Utilities
Duplicate Components
Duplicate Business Logic
```

---

# 9. Don't Assume File Names

Do not assume the project contains a file or Class with a specific name.

Search first.

Example:

Don't assume existence of:

```text
LeadService
```

Instead verify:

```text
services/
```

Then search for how the project organizes Lead services.

---

# 10. Understand Architecture Before Adding Logic

Must know which Layer the code belongs to.

Example:

```text
UI
  ↓
Service
  ↓
Repository
  ↓
Database
```

And external operations:

```text
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

Do not put Business Logic inside UI just because it's easier to implement there.

---

# 11. Choose the Least Appropriate Place for Modification

When fixing a problem, must identify the correct place for responsibility.

Example:

If error is in Business Logic:

```text
Fix Service
```

Not:

```text
Add workaround to UI
```

If error is in Query:

```text
Fix Repository
```

Not:

```text
Manipulate returned data in UI
```

---

# 12. Don't Use Unnecessary Workarounds

Avoid solutions that hide the problem instead of fixing it.

Bad:

```text
Database returns wrong data
→ Filter wrong data in UI
```

Better:

```text
Database Query
→ Fix Query
```

---

# 13. Minimal Change Principle

When executing a task, change the minimum number of files and lines necessary to achieve the requirement.

Do not rewrite working parts just to improve their style.

Avoid:

```text
Unnecessary Refactoring
Unrelated Cleanup
Mass Renaming
Large Rewrites
```

---

# 14. Don't Rewrite the Project

If the project works correctly, do not propose or execute a complete rebuild just because you see another way as better.

Priority:

```text
Preserve Existing Architecture
+
Improve Only What Is Necessary
```

---

# 15. Preserve Existing Behavior

When modifying an existing Feature:

```text
Existing Behavior
+
Requested Change
```

Not:

```text
Requested Change
-
Existing Behavior
```

Modification must not lead to removing Features or changing Behavior not requested.

---

# 16. Inspect Dependencies

Before adding a new Dependency:

```text
Search Existing Dependencies
Check if Existing Library Can Solve It
Check Project Requirements
```

Do not add a new library if the project already has a suitable solution.

---

# 17. Don't Add Abstraction Prematurely

Do not create:

```text
BaseClass
Factory
Manager
Helper
GenericService
Framework
```

Unless there is a clear reason.

Use the simplest design that meets current requirements and maintains Architecture.

---

# 18. Don't Duplicate Business Logic

If a rule exists in Service or Domain Logic, do not reimplement it in:

```text
UI
Repository
Collector
Parser
```

Must have a clear source for Business Logic.

---

# 19. Don't Put SQL Outside Database Layer

Do not write SQL inside:

```text
UI
Service
Validator
Collector
Parser
```

SQL must remain in Database/Repository Layer per Architecture.

---

# 20. Don't Put Database Logic Inside UI

UI must not:

```text
Open Database Connection
Execute SQL
Commit Transaction
Rollback Transaction
```

UI interacts with Services.

---

# 21. Don't Make Repository Contain Business Logic

Repository is responsible for:

```text
Data Access
Queries
Persistence
Mapping
```

Not:

```text
Lead Qualification
Duplicate Decision
Business Workflow
UI Decisions
```

---

# 22. Don't Make UI Contain Business Logic

UI is responsible for:

```text
Display
Input
Interaction
Navigation
UI State
```

And must not contain complex Business Rules.

---

# 23. Don't Make Collector Responsible for Database

Collector is responsible for data collection.

Correct flow:

```text
Collector
→ Parser
→ Validator
→ Service
→ Repository
```

Collector must not directly modify Database unless current Architecture is explicitly designed for that.

---

# 24. Separate Raw Data from Structured Data

When handling external data:

```text
Raw Data
→ Parsing
→ Normalization
→ Validation
→ Duplicate Detection
→ Business Processing
→ Persistence
```

Do not save external data directly to Database without passing through necessary steps.

---

# 25. Maintain Source Traceability

When processing Leads, Companies, or Contacts, do not lose data source.

If project stores Source information, must preserve it during:

```text
Import
Collection
Normalization
Update
Merge
Export
```

---

# 26. Don't Delete Data as Solution to Problem

If agent encounters:

```text
Duplicate
Constraint Error
Invalid Record
Conflict
Unexpected Data
```

Must not use:

```text
DELETE
```

As a quick fix.

Must first understand problem and apply Business Rules.

---

# 27. Don't Automatically Merge Duplicates

If system detects Duplicate:

```text
Confirmed Duplicate
Possible Duplicate
Not Duplicate
```

Must respect `business-rules.md`.

Especially:

```text
Possible Duplicate
→ Review
```

Not:

```text
Possible Duplicate
→ Automatic Merge
```

---

# 28. Don't Replace Good Data with Incomplete Data

When updating Record with new data:

```text
Existing Good Data
+
Incoming Incomplete Data
```

Must not automatically lead to:

```text
Existing Good Data
→ Empty / None
```

Must preserve correct information.

---

# 29. Don't Assume Error Comes from Apparent Place

When Error occurs:

Do not directly assume the last modified file is the cause.

Follow:

```text
Error
→ Trace
→ Root Cause
→ Correct Layer
→ Fix
```

---

# 30. Fix Root Cause

If occurs:

```text
Database Constraint Error
```

Do not hide error with:

```text
try:
    ...
except:
    pass
```

Instead understand:

```text
Why did invalid data reach Database?
```

Then fix cause in appropriate place.

---

# 31. Don't Hide Exceptions

Forbidden to use:

```python
try:
    ...
except:
    pass
```

Or:

```python
except Exception:
    return None
```

If it hides a real Failure.

Must follow `error-handling.md` rules.

---

# 32. Don't Claim Success

If operation fails:

```text
Save Failed
Export Failed
Import Failed
Collection Failed
Update Failed
```

Do not display Success to user.

---

# 33. Test After Modification

After any significant modification:

```text
Modify
→ Run Related Tests
→ Check Result
```

And after major modifications:

```text
Run Relevant Unit Tests
→ Run Integration Tests
→ Run Critical Workflow Tests
```

---

# 34. Don't Rely on Guessing in Tests

If Test fails:

```text
Investigate Failure
```

And do not change Assert just to make test pass.

Must determine:

```text
Is Code Wrong?
Is Test Wrong?
Did Business Rule Change?
Did Expected Behavior Change?
```

---

# 35. Add Regression Test for Important Bugs

If fixed an important Bug:

```text
Reproduce Bug
→ Add Test
→ Fix Bug
→ Test Passes
```

And must keep test so error doesn't return in future.

---

# 36. Verify Modification Impact

Before considering task complete, ask:

```text
What else depends on this code?
```

Especially when modifying:

```text
Models
Services
Repositories
Database Schema
Shared Utilities
Business Rules
Navigation
Shared UI Components
```

---

# 37. Don't Break Internal APIs Without Reason

If Classes or Services are used in multiple places, do not change:

```text
Function Signature
Class Interface
Return Structure
Expected Behavior
```

Without verifying all usages.

---

# 38. Search All Usages Before Changing

Before changing:

```text
Function
Class
Method
Database Column
Service
Repository Method
Shared Component
```

Search for places that use it.

Flow:

```text
Definition
+
All References
+
Tests
→
Safe Modification
```

---

# 39. Database Changes Need Extra Caution

Before modifying Database:

```text
Inspect Current Schema
→ Identify Dependencies
→ Check Business Rules
→ Determine Impact
→ Make Minimal Change
→ Update Relevant Code
→ Test
```

Do not assume modifying one Column doesn't affect rest of project.

---

# 40. Don't Recreate Full Schema Unnecessarily

If requirement is:

```text
Add Column
```

Do not automatically rewrite entire Database Schema.

Use Minimal Schema Change.

---

# 41. Respect Existing Data

Any Database modification must respect existing data.

Before modification ask:

```text
Will existing records remain valid?
Will relationships remain valid?
Will existing queries continue working?
```

---

# 42. Transaction Safety

When there's a multi-step operation:

```text
Step A
Step B
Step C
```

If they must succeed as one unit, use appropriate Transaction.

If Step C fails:

```text
Rollback
```

Per `database-rules.md` and `error-handling.md`.

---

# 43. Don't Use Production Data for Tests

Tests must use:

```text
Test Database
Fixtures
Synthetic Data
Mocks/Fakes
```

And must not modify user's real Database.

---

# 44. External Services

When dealing with:

```text
Websites
APIs
Network
External Services
```

Do not make Unit Tests depend on them.

Use:

```text
Mock
Fake
Stub
Fixture
```

When needed.

---

# 45. Handling Long Operations

If operation is:

```text
Collection
Import
Export
Large Processing
```

Long-running, must consider:

```text
Progress
Cancellation
Error Recovery
Resource Cleanup
UI Responsiveness
```

And must not execute heavy operation in a way that freezes UI if Architecture provides suitable background operation mechanism.

---

# 46. Don't Add Features User Didn't Request

If user requests:

```text
Add Search
```

Do not automatically add:

```text
Dashboard
Charts
Analytics
Notifications
AI Recommendations
```

Unless required or necessary to achieve the task.

---

# 47. Don't Add Unnecessary UI

Respect `ui-guidelines.md`.

Do not add:

```text
Unnecessary Cards
Animations
Charts
Tabs
Dialogs
KPI Widgets
```

Just to make page look more complex.

---

# 48. Ask Only When Needed

Agent must not stop work due to details that can be safely inferred from:

```text
Existing Code
Skills
Architecture
Business Rules
Project Structure
```

But must ask when decision is:

```text
Ambiguous
Destructive
Architecture-changing
Data-affecting
Business-critical
```

And there's insufficient basis to make it.

---

# 49. Before Dangerous Operations

Must stop and request clear confirmation before operations that could lead to:

```text
Permanent Data Loss
Mass Deletion
Destructive Migration
Large Architecture Rewrite
Removing Important Features
Breaking Public Interfaces
```

Do not assume these operations are acceptable just because they're implementable.

---

# 50. Understand Difference Between "Fix" and "Refactor"

If user requests:

```text
Fix Bug
```

Priority:

```text
Minimal Safe Fix
```

Not:

```text
Rewrite Entire Module
```

If user requests Refactoring, can expand scope of change, but must preserve Behavior and use Tests.

---

# 51. Understand Difference Between "Improve" and "Rewrite"

"Improve" doesn't automatically mean:

```text
Replace Existing Architecture
```

Must determine:

```text
What is actually being improved?
```

Then implement only the appropriate change.

---

# 52. Don't Create Files Just for Organization

Every new File must have a clear Responsibility.

Before creating File:

```text
Does this responsibility already have a home?
```

If yes, use existing unless there's a clear architectural reason to separate.

---

# 53. Shared Code

If Function or Component is used in more than one place:

```text
Consider Shared Location
```

But don't move code to Shared Utility just because it can be done.

Sharing must be real and justified.

---

# 54. Avoid Circular Dependencies

Before adding Import:

```text
Check Dependency Direction
```

Must maintain general direction:

```text
UI
  ↓
Services
  ↓
Repositories
  ↓
Database
```

And lower layers must not depend on UI.

---

# 55. Maintain Naming Conventions

Before creating:

```text
File
Class
Function
Variable
Database-related Code
```

Check `coding-rules.md` and existing conventions in project.

Do not create new Naming Style inside project.

---

# 56. Use Existing Patterns

If project has a clear Pattern:

```text
Existing Service
Existing Repository
Existing Validator
Existing UI Page
Existing Dialog
```

Prefer following it instead of creating different Pattern without reason.

---

# 57. Don't Improve Everything During Task

If you notice:

```text
Unrelated Code Smell
Old Naming
Minor Refactor Opportunity
```

Don't change automatically if not necessary for task.

Can point it out only if important.

---

# 58. Don't Leave Debug Code

Before finishing task, ensure not leaving:

```text
print()
Temporary Debugging
Commented-out Code
Hardcoded Test Values
Temporary Files
Unused Imports
Dead Code
```

Unless their presence is intentional.

---

# 59. Don't Use Hardcoded Configuration

Do not put:

```text
API Keys
Passwords
Database Credentials
Machine-specific Paths
```

Inside Source Code.

Use appropriate Configuration per project.

---

# 60. Handle External Data with Caution

Data coming from:

```text
Websites
Files
APIs
Users
Imports
```

Must be considered untrusted until:

```text
Parse
Normalize
Validate
```

And must not assume external data is correct.

---

# 61. Don't Trust Field Names from External Sources

When Importing or Parsing, verify:

```text
Required Fields
Types
Formats
Encoding
Unexpected Columns
Missing Columns
```

Per project rules.

---

# 62. Don't Make AI Repeat Same Logic

Before writing new Function, search for:

```text
Similar Function
Equivalent Utility
Existing Service Method
Existing Validator
```

If suitable solution found, use or extend it instead of copying logic.

---

# 63. Don't Hide Problem Complexity

If task requires modifying multiple Layers:

```text
UI
+
Service
+
Repository
+
Database
```

Don't try to put everything in one file just to reduce modified file count.

Correct approach is to respect Architecture.

---

# 64. Plan Before Large Changes

When there's a large task, create clear internal plan:

```text
1. Understand
2. Inspect
3. Identify affected files
4. Identify rules
5. Identify risks
6. Implement
7. Test
8. Verify
```

Do not start modifying files randomly.

---

# 65. Implementation Order

When needing to modify multiple Layers, prefer logical order:

```text
Domain / Data Requirements
        ↓
Database / Repository
        ↓
Service / Business Logic
        ↓
Validation
        ↓
UI
        ↓
Tests
```

But follow current Architecture if project uses different order.

---

# 66. Review Diff After Modification

Before finishing task, must review changes to ensure:

```text
Only Intended Files Changed
No Accidental Changes
No Debug Code
No Unused Imports
No Unrelated Refactoring
No Broken Formatting
No Secrets
```

---

# 67. Verify New Files

Any new File must verify:

```text
Correct Location
Correct Naming
Correct Imports
Correct Responsibility
Used Where Necessary
Tested When Relevant
```

---

# 68. Verify Imports

After modifications:

```text
No Circular Import
No Unused Import
No Missing Import
No Incorrect Import Path
```

---

# 69. Verify Compatibility

After modifying internal API or Service:

```text
Search Callers
Update Dependent Code
Run Tests
```

Do not leave parts of project using old Interface.

---

# 70. Don't Assume "No Error" Means "Correct"

Program may run without Exception while Behavior is wrong.

Therefore verify:

```text
Expected Output
Expected Database State
Expected Business Behavior
Expected UI Behavior
```

---

# 71. Definition of Done

Do not consider task complete until verified:

```text
[ ] Requirement understood
[ ] Relevant Skills checked
[ ] Existing code inspected
[ ] Existing patterns checked
[ ] Correct layer identified
[ ] Minimal change implemented
[ ] Business rules respected
[ ] Database rules respected
[ ] Error handling respected
[ ] Relevant tests added/updated
[ ] Tests executed
[ ] No unrelated changes
[ ] No debug code
[ ] No accidental data loss
[ ] Final behavior verified
```

---

# 72. If Tests Fail

Follow:

```text
Test Failure
    ↓
Read Error
    ↓
Identify Failing Component
    ↓
Trace Root Cause
    ↓
Fix Correct Layer
    ↓
Run Related Test
    ↓
Run Broader Tests
```

Do not use:

```text
Disable Test
Delete Test
Weaken Assertion
Ignore Failure
```

As quick fix.

---

# 73. If Not Sure

Use this order:

```text
Project Skills
        ↓
Existing Code
        ↓
Existing Tests
        ↓
Existing Patterns
        ↓
Architecture
        ↓
Business Rules
        ↓
Ask User if still ambiguous
```

Do not use guessing as substitute for understanding project.

---

# 74. Safe Change Rule

Every change must be:

```text
Necessary
+
Minimal
+
Consistent
+
Tested
+
Reversible where practical
```

---

# 75. Non-Destruction Rule

Agent must be:

```text
Non-destructive
```

And must prefer:

```text
Update
+
Preserve
+
Review
```

Over:

```text
Delete
+
Overwrite
+
Replace
```

Especially for Leads, Companies, Contacts, and Domains data.

---

# 76. Clarity Rule

Code written by agent must be understandable by developer who reads it later.

Avoid:

```text
Clever Tricks
Overengineering
Unnecessary Abstractions
Compressed Logic
Hidden Side Effects
```

Priority:

```text
Readable
Predictable
Maintainable
```

---

# 77. Continuity Rule

Agent must act as if working on an existing project, not a new one starting from scratch.

Therefore:

```text
Respect Existing Structure
Respect Existing Naming
Respect Existing Patterns
Respect Existing Data
Respect Existing Behavior
```

---

# 78. No Guessing in Data Rule

Do not create:

```text
Company
Contact
Email
Domain
Lead
```

With unconfirmed information just to complete operation.

If data is unconfirmed, must follow rules:

```text
Validation
Duplicate Detection
Review
Source Preservation
```

---

# 79. Traceability Rule

Must be possible to understand:

```text
Where did this data come from?
Why was it created?
Why was it updated?
Why was it classified as duplicate?
Why did the system reject it?
```

When Architecture and Database provide ability to save this information, must not lose it.

---

# 80. Important Rule for AI Agent

Do not execute instructions literally if obvious result will break Architecture or Business Rules.

Understand:

```text
User Intent
+
Project Constraints
```

Then implement solution that achieves requirement correctly within project.

---

# 81. Rule for Handling Modification Requests

When receiving request like:

```text
"Add Feature X"
```

Follow:

```text
Understand X
→ Find related code
→ Check Skills
→ Identify affected layers
→ Check existing implementation
→ Plan minimal change
→ Implement
→ Test
→ Verify
```

---

# 82. Rule for Handling Fix Requests

When receiving:

```text
"There's an error in X"
```

Follow:

```text
Reproduce
→ Inspect
→ Trace
→ Identify Root Cause
→ Add/Update Regression Test
→ Fix
→ Run Tests
→ Verify
```

---

# 83. Rule for Handling UI Requests

When receiving:

```text
"Improve the page"
```

Must first understand:

```text
Current UI
Current Components
Current Navigation
Current UI Guidelines
```

Then make visual and functional improvement without putting Business Logic inside UI.

---

# 84. Rule for Handling Database Requests

When receiving:

```text
"Modify Database"
```

Must:

```text
Inspect Schema
→ Check Relationships
→ Check Business Rules
→ Check Existing Queries
→ Determine Impact
→ Make Minimal Change
→ Update Code
→ Test
```

---

# 85. Rule for Handling Collector Requests

When receiving:

```text
"Add a new data source"
```

Must think in terms of:

```text
Collection
→ Parsing
→ Normalization
→ Validation
→ Duplicate Detection
→ Business Processing
→ Persistence
```

And not put all these responsibilities inside one Collector.

---

# 86. Rule for Handling Import Requests

Correct flow:

```text
Read
→ Parse
→ Normalize
→ Validate
→ Duplicate Detection
→ Review when needed
→ Save
→ Report Result
```

Must not bypass Validation and Duplicate Detection just to speed up process.

---

# 87. Rule for Handling Export Requests

Flow:

```text
Select Data
→ Prepare
→ Export
→ Verify Success
→ Report Result
```

If Export fails, do not display Success.

---

# 88. Rule for Preserving Tests

When modifying code:

```text
Existing Tests
```

Are not obstacles to change, but protection against Regression.

If Behavior changes intentionally, update Tests per new Behavior.

---

# 89. Behavior Priority Rule

When choosing between:

```text
Elegant Code
```

And:

```text
Correct Behavior
```

Priority goes to correct behavior.

And when choosing between:

```text
Quick Implementation
```

And:

```text
Safe Implementation
```

Priority goes to safe solution.

---

# 90. Final AI Development Workflow

Agent must follow this Workflow as general rule:

```text
┌──────────────────────┐
│ 1. Understand Request│
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 2. Read Relevant     │
│    Skills            │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 3. Inspect Project   │
│    and Existing Code  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 4. Identify Correct  │
│    Layer and Files    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 5. Check Dependencies │
│    and Impact         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 6. Plan Minimal      │
│    Safe Change        │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 7. Implement         │
│    Correctly          │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 8. Run Tests         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 9. Review Changes    │
│    and Side Effects   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ 10. Verify Final     │
│     Behavior          │
└──────────────────────┘
```

---

# 91. Concise Rules Agent Must Not Forget

```text
1. Understand before coding.
2. Inspect before modifying.
3. Read relevant Skills.
4. Never guess existing structure.
5. Search before creating new code.
6. Respect Architecture.
7. Respect Business Rules.
8. Respect Database Rules.
9. Keep responsibilities separated.
10. Prefer minimal changes.
11. Preserve existing behavior.
12. Do not rewrite working code unnecessarily.
13. Do not duplicate logic.
14. Do not hide errors.
15. Do not delete data as a workaround.
16. Do not automatically merge uncertain duplicates.
17. Preserve source and traceability.
18. Test important changes.
19. Add regression tests for important bugs.
20. Never weaken tests just to make them pass.
21. Review the final diff.
22. Remove debug code.
23. Check for accidental side effects.
24. Ask only when ambiguity materially affects the result.
25. When in doubt, inspect rather than guess.
```

---

# 92. Golden Rule

Agent must not ask:

```text
"What code can I write?"
```

But:

```text
"What is the correct change for this existing system?"
```

Then:

```text
Understand
→ Inspect
→ Plan
→ Change
→ Test
→ Verify

This project must evolve **incrementally and safely**, not through continuous rewrites or random changes.
