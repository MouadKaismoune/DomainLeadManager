---
name: error-handling
description: Defines error handling rules for the agent to handle errors safely and clearly, especially SQLite, input, file, network, and data collection errors, while preventing error hiding or data loss.
---

# Error Handling

## 1. Purpose

This skill defines error handling rules within the project.

The Error Handling system must be:

* Clear.
* Safe.
* Traceable.
* Testable.
* User-friendly.
* Developer-friendly.
* Non-destructive to data.
* Compatible with project Architecture.

Errors must not lead to:

* Data loss.
* Unintentional data deletion.
* Problem hiding.
* Full application crash due to a handleable error.
* Displaying inappropriate technical details to the user.

---

# 2. Fundamental Principle

Do not hide errors.

When an error occurs:

```text
Detect
→ Handle
→ Log
→ Inform
→ Recover or Stop Safely
```

Must be clear:

* What happened?
* Where did it happen?
* Why did it happen (if possible)?
* Can we continue?
* What action is required?

---

# 3. Don't Use Bare Except

Forbidden:

```python
try:
    ...
except:
    pass
```

And forbidden:

```python
try:
    ...
except Exception:
    pass
```

Because this hides errors and makes Debugging difficult.

---

# 4. Don't Use Silent Failure

Do not make a Function fail silently.

Bad:

```python
def save_company(company):
    try:
        repository.save(company)
    except Exception:
        return None
```

If failure is important, must log it or raise an appropriate Exception or return a clear result per Architecture.

---

# 5. Catch Specific Exceptions

Catch specific Exceptions when possible.

Example:

```python
try:
    value = int(user_input)
except ValueError:
    ...
```

Better than:

```python
try:
    value = int(user_input)
except Exception:
    ...
```

Use general `Exception` only when there's an actual need.

---

# 6. Don't Use Exceptions for Normal Flow Control

Do not use Exception to handle an expected case that can be dealt with normally.

Bad:

```python
try:
    company = companies[index]
except IndexError:
    company = None
```

If it's possible to check the Index before accessing it, that's clearer.

But if the Exception is a natural part of an API or Database operation, it can be handled appropriately.

---

# 7. Error Categories

Must distinguish between error types.

Main types:

```text
Validation Errors
Input Errors
Database Errors
File Errors
Network Errors
Collection Errors
Parsing Errors
Permission Errors
Configuration Errors
Unexpected Errors
```

Each type must be handled in the appropriate layer.

---

# 8. Validation Errors

Validation Error means data exists but is incorrect.

Examples:

```text
Invalid email
Invalid domain
Missing company name
Invalid lead status
Invalid phone number
Invalid imported data
```

Must not save invalid data if Business Rules prevent it.

---

# 9. User Input Errors

User data may be:

```text
Empty
Incorrect
Incomplete
Out of range
Wrong format
```

Must validate before executing the operation.

Example:

```python
if not company_name.strip():
    raise ValidationError("Company name is required")
```

But the message reaching the UI must be user-appropriate.

---

# 10. Don't Rely on UI Only for Validation

Validation must not exist only in UI.

Example:

```text
UI Validation
+
Business Validation
+
Database Constraints
```

UI can prevent obviously wrong input, but Service/Domain layer must also protect Business Rules.

---

# 11. Database Errors

Database errors must be handled carefully.

Examples:

```text
Connection failure
Database locked
Constraint violation
Foreign key violation
Unique constraint violation
Invalid SQL
Transaction failure
Database file unavailable
```

Do not expose internal SQL details to the user unless necessary for development.

---

# 12. Database Connection Errors

If unable to connect to the database:

1. Log the error.
2. Do not start operations that depend on Database.
3. Show a clear message to the user.
4. If possible, allow retry.
5. Do not create fake data instead of Database.

Example user message:

```text
Unable to connect to the database.
Please check the database configuration and try again.
```

---

# 13. Database Locked

In SQLite, may occur:

```text
database is locked
```

Do not handle by ignoring the error.

Can:

* Log the error.
* Retry in a limited way if appropriate.
* Use Transactions correctly.
* Reduce Transaction open duration.
* Ensure Connections are managed correctly.

Do not use Infinite Retry.

---

# 14. Unique Constraint Errors

If occurs:

```text
UNIQUE constraint violation
```

Do not automatically delete the existing record.

And do not replace existing data without a Business Rule allowing it.

Must:

```text
Detect
→ Understand conflict
→ Inform/Resolve
```

Example:

```text
A company with this domain already exists.
```

---

# 15. Foreign Key Errors

If an operation fails due to Foreign Key:

Do not bypass Constraint just to complete the operation.

Must know:

* What is the related record?
* Why is it missing?
* Is the data incomplete?
* Is the operation in the wrong order?

Then address the cause.

---

# 16. Transaction Errors

When an operation contains multiple Database operations:

```text
Operation A
Operation B
Operation C
```

And B fails, must not leave Database in a partial state if the operation must be Atomic.

Use:

```text
BEGIN
→ operations
→ COMMIT
```

Or:

```text
BEGIN
→ operations
→ ROLLBACK
```

On failure.

---

# 17. Rollback

When Transaction fails:

```python
try:
    ...
    connection.commit()
except Exception:
    connection.rollback()
    raise
```

Must not partially Commit an operation that was supposed to be Atomic.

---

# 18. Do Not Swallow Database Errors

Forbidden:

```python
try:
    cursor.execute(query)
except Exception:
    return []
```

If Database failure means results are unknown.

Returning an empty list may imply:

```text
No data found
```

While the truth is:

```text
Database operation failed
```

This is an important difference.

---

# 19. Distinguish "No Data" from "Error"

These are two different states:

```text
No results
```

And:

```text
Failed to retrieve results
```

Must not represent them with the same value.

Example:

```python
[]
```

Can mean no data found, so do not use it to hide Database Error.

---

# 20. File Errors

When dealing with files, expect:

```text
File not found
Permission denied
Invalid path
Invalid format
Encoding error
File already exists
Disk full
File locked
```

Must handle them clearly.

---

# 21. File Not Found

If file doesn't exist:

Do not assume the file exists.

Handle the state clearly:

```python
if not file_path.exists():
    ...
```

Or handle `FileNotFoundError` when more appropriate.

---

# 22. File Permission Errors

If the program cannot read or write a file:

* Log the error.
* Tell the user that Permission is the problem.
* Do not attempt to bypass the OS or permissions in an unsafe way.

Example:

```text
The application does not have permission to access this file.
```

---

# 23. Import Errors

When importing CSV, Excel, or JSON:

Must handle:

```text
Invalid format
Missing columns
Invalid encoding
Corrupted file
Invalid values
Duplicate records
Unexpected structure
```

Do not save partial data unexpectedly.

---

# 24. Import Validation

Import process must be:

```text
Read
→ Parse
→ Validate
→ Detect duplicates/conflicts
→ Review if necessary
→ Save
```

Not:

```text
Read
→ Save everything
```

---

# 25. Partial Import Failures

If a file contains 1000 Records and one Record fails:

Do not automatically assume all Records must fail.

But also do not save Partial Data without knowing the Import policy.

Must clearly define if the process is:

```text
Atomic Import
```

Or:

```text
Partial Import
```

Per project requirements.

If Partial Import is allowed, must show:

```text
Imported successfully
Failed
Skipped
Duplicates
Invalid
```

---

# 26. Export Errors

When Exporting:

If file creation fails:

* Do not show the user that Export succeeded.
* Log the reason.
* Inform the user of the failure.
* Do not create an incomplete file and consider it valid.

Example:

```text
Export failed.
The file could not be created.
```

---

# 27. Temporary Files

When using Temporary Files:

* Use an appropriate path.
* Handle creation failure.
* Clean up temporary files after completion when possible.
* Do not delete user files.

---

# 28. Encoding Errors

Because the project may handle:

```text
Arabic
French
English
```

Must handle Encoding Errors clearly.

Use UTF-8 by default when appropriate.

Do not delete unsupported characters or replace them silently.

---

# 29. Parsing Errors

Parsing Error occurs when data cannot be analyzed in the expected format.

Example:

```text
HTML structure changed
Invalid JSON
Malformed CSV
Unexpected column
Invalid email structure
```

Must:

1. Log the error.
2. Retain useful context.
3. Do not create incorrect data.
4. Return an appropriate Error to the upper layer.

---

# 30. Collection Errors

In Data Collection, one source may fail while others continue.

Must not automatically stop the entire process unless the error is Critical.

Example:

```text
Source A → Success
Source B → Failed
Source C → Success
```

Can continue the process if Architecture allows it.

But must log:

```text
Source B failed
```

And show the result to the user.

---

# 31. Network Errors

When dealing with Internet/API:

Expect:

```text
Timeout
Connection Error
DNS Error
HTTP Error
Rate Limit
Authentication Error
Invalid Response
Server Error
```

Must handle them according to the error type.

---

# 32. Timeouts

Must not execute a Network Request without a Timeout when the library/operation allows it.

Do not make the program wait indefinitely.

---

# 33. Retry Policy

Retry can be used for temporary errors like:

```text
Timeout
Temporary connection failure
Temporary server error
```

But:

* Number of attempts must be limited.
* Do not use Retry for permanent errors.
* Do not use Infinite Retry.
* Do not repeat operations that may cause Duplicate Data without ensuring Idempotency.

---

# 34. Rate Limits

If an external source returns:

```text
429 Too Many Requests
```

Do not continue sending Requests at a faster rate.

Must respect the Rate Limit and source policy.

Can use:

```text
Backoff
Retry-After
Request throttling
```

If appropriate.

---

# 35. Authentication Errors

When an Authentication Error occurs:

Do not repeat the request infinitely.

Like:

```text
Invalid API key
Expired token
Unauthorized
```

Must stop the process or request reconfiguration of Credentials per Architecture.

---

# 36. HTTP Errors

Must distinguish between:

```text
4xx
5xx
```

4xx errors often need Request, permission, or data correction.

5xx errors may be temporary and can have limited Retry for some cases.

---

# 37. User-Friendly Errors

The user doesn't usually need:

```text
sqlite3.IntegrityError:
UNIQUE constraint failed: companies.domain
```

Instead can display:

```text
A company with this domain already exists.
```

While logging technical details in Logs.

---

# 38. Developer Logs vs User Messages

Must separate:

```text
User Message
```

And:

```text
Developer Log
```

Example User:

```text
Could not save the company.
Please try again.
```

Log:

```text
Failed to save company: IntegrityError(...)
```

---

# 39. Never Expose Secrets

Do not put inside Error Message or Logs:

```text
API keys
Passwords
Tokens
Credentials
Sensitive authentication data
```

Even when an Exception occurs.

---

# 40. Logging Exceptions

When an Unexpected Error occurs, must log Stack Trace in Logs when appropriate.

Do not just log:

```text
Something went wrong
```

In Log.

Must allow the developer to know the error location.

---

# 41. Unexpected Errors

Unexpected errors must not lead to hiding the problem.

Can use a Global Error Handler at the application level for:

* Logging the Exception.
* Preventing unorganized Crash.
* Showing a safe message.
* Allowing the user to return to a stable state.

But Global Handler is not a substitute for proper error handling in appropriate layers.

---

# 42. Global Error Handler

Can have a central point for handling unhandled Errors.

Its responsibility:

```text
Catch unexpected errors
→ Log full details
→ Show safe user message
→ Keep application stable when possible
```

Must not be used to hide Business Logic errors.

---

# 43. Error Propagation

If the current layer cannot handle the error properly, must raise it to the upper layer.

Example:

```text
Repository
    ↓ raises
Service
    ↓ handles/translates
UI
    ↓ displays
User
```

Do not make Repository show a Message Box to the user.

---

# 44. Repository Error Responsibility

Repository is responsible for:

* Database Errors.
* Query Errors.
* Transaction Errors.

But Repository must not know:

```text
UI
Dialogs
Pages
Message boxes
```

It can raise an appropriate Exception to the Service.

---

# 45. Service Error Responsibility

Service is responsible for Business-Level Errors.

Example:

```text
Company already exists
Invalid lead transition
Duplicate relationship
Required entity missing
```

Service can convert Low-Level Errors into understandable Domain Errors.

---

# 46. UI Error Responsibility

UI is responsible for:

* Displaying the Error to the user.
* Determining the appropriate place to display it.
* Allowing retry if appropriate.
* Not exposing unnecessary Technical Details.

UI must not handle every Error through `except Exception`.

---

# 47. Error Messages

Error Messages must be:

* Clear.
* Short.
* Useful.
* Actionable when possible.

Bad:

```text
Error 0x000034A
```

Better:

```text
The selected file could not be opened.
Please check that it exists and that you have permission to access it.
```

---

# 48. Avoid Technical Details in User Messages

Do not display:

```text
Stack trace
SQL query
File system internals
Python exception object
API credentials
```

To the regular user.

These belong in Logs.

---

# 49. Error Codes

Can use Error Codes when the project needs them.

Example:

```text
DB_CONNECTION_FAILED
FILE_NOT_FOUND
INVALID_EMAIL
DUPLICATE_COMPANY
IMPORT_FAILED
```

But do not create a complex Error Code system if there's no real need.

---

# 50. Domain Exceptions

Can create Domain-specific Exceptions in:

```text
app/core/exceptions.py
```

Or the location specified in Architecture.

Examples:

```python
class ValidationError(Exception):
    pass


class DuplicateEntityError(Exception):
    pass


class BusinessRuleError(Exception):
    pass
```

Must not create dozens of Exceptions without need.

---

# 51. Exception Chaining

When converting a low-level Exception to a higher-level one, preserve the cause when useful.

Example:

```python
try:
    ...
except DatabaseError as exc:
    raise RepositoryError("Failed to load company") from exc
```

This preserves the Root Cause.

---

# 52. Root Cause

Do not treat the Symptom only.

Example:

If fails:

```text
Save Lead
```

Do not make the solution:

```python
except:
    return False
```

Find the cause:

```text
Invalid data?
Database constraint?
Missing relationship?
Connection problem?
Programming bug?
```

---

# 53. Error Recovery

When Recovery is possible and safe, use it.

Examples:

```text
Retry
Reconnect
Rollback
Reopen
Skip invalid record
Allow user to correct input
```

But Recovery must not lead to Data Loss.

---

# 54. Safe Failure

If Recovery is not possible:

```text
Stop the current operation safely.
```

Do not complete an operation that could lead to Database corruption or incorrect data.

---

# 55. No Automatic Data Destruction

Error Handling must not turn into automatic Data Cleanup.

Forbidden when an Error occurs:

```text
delete duplicate
delete invalid record
delete company
delete contact
delete lead
```

Unless it's an explicit part of a user-requested process and project rules allow it.

---

# 56. Duplicate Errors

If the system detects a Duplicate:

Do not always treat it as a regular Exception.

The result may be:

```text
Confirmed Duplicate
Possible Duplicate
Not Duplicate
```

Per `business-rules.md`.

Do not automatically delete or merge data due to Error Handling.

---

# 57. Preserve User Data

If a Save or Update operation fails:

Do not wipe User Input without reason.

Example:

If Save fails due to Database Error, must preserve the entered data as much as possible so the user can:

```text
Retry
Edit
Cancel
```

---

# 58. UI State After Error

After an Error occurs, the UI must be in a correct state.

Example:

If Save fails:

```text
Loading → Error
```

Not:

```text
Loading → Nothing
```

Must restore buttons and state to a condition that allows the user to try again if possible.

---

# 59. Progress Operations

In long Collection or Import/Export operations:

If an Error occurs:

* Stop the current operation or handle it per error type.
* Show Progress/Failure state.
* Do not make the UI look like the operation is still running.
* Retain successful results if the process allows it.
* Clarify what failed.

---

# 60. Cancellation

If the user can cancel a long operation, must handle Cancellation safely.

Do not leave:

```text
Database Transaction
File
Network connection
Temporary resource
```

In an unsound state.

---

# 61. Resource Cleanup

When an Error occurs, must clean up resources that were opened.

Like:

```text
Files
Database cursors
Connections
Temporary files
Network resources
```

Use Context Managers or appropriate Cleanup mechanisms.

---

# 62. Logging Levels

Use appropriate Logging Levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Roughly:

```text
DEBUG
→ Developer information during development

INFO
→ Important normal operations

WARNING
→ Non-critical problem or unexpected state

ERROR
→ Operation failed

CRITICAL
→ Serious problem affecting the entire application
```

---

# 63. Do Not Over-Log

Do not log everything randomly.

Avoid huge Logs that cannot be read.

Focus on:

* Important operations.
* Errors.
* Warnings.
* Useful diagnostic information.

---

# 64. Log Context

When logging an Error, add useful Context without exposing sensitive data.

Example:

```text
Operation: import_leads
Source: csv_import
Records: 500
Failed record index: 42
Error: invalid email
```

This is better than:

```text
Error occurred
```

---

# 65. No Sensitive Data in Logs

Do not log:

```text
Passwords
API Keys
Tokens
Full credentials
```

And do not log personal data more than needed for diagnosis.

---

# 66. Error Handling in Batch Operations

When processing multiple Records:

```text
Lead 1
Lead 2
Lead 3
...
```

Must determine if an error in one Record is:

```text
Record-level failure
```

Or:

```text
Operation-level failure
```

A single Record error must not stop the entire Batch if continuing is safe and allowed.

---

# 67. Batch Error Reporting

After a Batch Operation, can show a summary:

```text
Processed: 500
Succeeded: 470
Skipped: 20
Failed: 10
```

If the process supports this type of result.

Must not consider failed Records as successful.

---

# 68. Error Result Objects

If a complex operation needs more than Success/Failure, can use a clear Result Object.

Example:

```python
@dataclass
class OperationResult:
    success: bool
    processed: int
    failed: int
    skipped: int
    errors: list[str]
```

But do not use this Pattern in every simple Function.

---

# 69. Validation vs Exception

Not every Invalid Input needs an Exception.

In UI it can be:

```text
Validation Result
```

Better than Throwing an Exception for every character the user types.

But Business Rule violations or internal layer errors may be appropriate for Exceptions.

Use the simplest and clearest approach for each case.

---

# 70. Testing Error Handling

Must test important cases, not just Success.

Test:

```text
Database unavailable
Database locked
Constraint violation
Invalid input
Missing file
Invalid file
Permission error
Network timeout
HTTP error
Invalid response
Duplicate record
Transaction rollback
Unexpected exception
```

---

# 71. Test Recovery

If there's Retry, Rollback, or Recovery, must test it.

Example:

```text
Operation fails
→ rollback
→ database remains consistent
```

Must verify this actually happens.

---

# 72. Error Handling Must Not Hide Bugs

Do not use Error Handling to cover up Bugs in the code.

If there's:

```python
NameError
AttributeError
TypeError
```

Due to a Programming Bug, do not make:

```python
except Exception:
    ...
```

Hide it during development.

Must appear in Logs and be diagnosable.

---

# 73. Development vs Production

In Development:

* Errors must be easy to diagnose.
* Must log Stack Traces.
* Do not hide Bugs.

In Production:

* Do not show Stack Trace to the user.
* Log details in Logs.
* Show a safe and understandable message.

---

# 74. Error Handling Flow

Preferred flow:

```text
Operation
    ↓
Error occurs
    ↓
Identify error type
    ↓
Handle at the correct layer
    ↓
Rollback / Cleanup / Retry if appropriate
    ↓
Log useful technical details
    ↓
Translate to user-friendly message if needed
    ↓
Return application to safe state
```

---

# 75. Error Handling and Architecture

Must respect Architecture:

```text
UI
  ↓
Services
  ↓
Repositories
  ↓
Database
```

Example:

```text
Database Exception
        ↓
Repository
        ↓
Service / Domain Error
        ↓
UI
        ↓
User-friendly message
```

Do not make:

```text
Repository → MessageBox
```

Or:

```text
Database → UI
```

---

# 76. Error Handling and Business Rules

Error Handling must not violate `business-rules.md`.

Especially:

```text
Duplicate Detection
No automatic merge
No automatic deletion
Preserve existing data
Lead status rules
Source traceability
```

When a Conflict exists, must preserve data instead of automatically making a destructive decision.

---

# 77. Error Handling and Database Rules

Must respect `database-rules.md`.

Especially:

```text
Transactions
Foreign Keys
Constraints
Parameterized Queries
Data Integrity
Repository Pattern
```

Error Handling must not bypass Database Constraints just to avoid an Error.

---

# 78. Error Handling and Coding Rules

Must also respect `coding-rules.md`.

Especially:

```text
No bare except
Specific exceptions
Clear functions
Logging
Separation of concerns
No hidden side effects
Testability
```

---

# 79. AI Agent Rules

When encountering an Error during project development, the agent must:

1. Read the Error Message completely.
2. Identify the error type.
3. Identify the layer where it occurred.
4. Check the Root Cause.
5. Do not add `except Exception` to hide it.
6. Do not delete data to bypass the problem.
7. Do not change Architecture without need.
8. Fix the cause instead of hiding the result.
9. Test the fix.
10. Ensure no Regression appears.

---

# 80. Before Fixing an Error

Before fixing the error:

```text
Read traceback
→ Locate failing code
→ Understand inputs
→ Check related modules
→ Check business rules
→ Check database rules
→ Identify root cause
→ Apply minimal fix
→ Test
```

Do not rely on a quick guess from the error message only.

---

# 81. Minimal Error Fix

When fixing a Bug:

Do not automatically rewrite an entire Module.

Use:

```text
Smallest correct fix
```

Unless inspection proves the problem needs larger Refactoring.

---

# 82. Do Not Mask Errors

Forbidden to use solutions like:

```python
try:
    operation()
except Exception:
    return True
```

Or:

```python
except Exception:
    return []
```

Or:

```python
except Exception:
    pass
```

If these values mislead the upper layer into thinking the operation succeeded.

---

# 83. Success Must Mean Success

Do not return:

```text
True
```

Unless the operation actually succeeded.

And do not display:

```text
Success
```

If an Error occurred.

This is an important rule especially in:

```text
Save
Import
Export
Collection
Update
Delete
Database operations
```

---

# 84. Final Safety Rule

When in doubt, choose the safest behavior for data.

Priority:

```text
Data Integrity
→ Traceability
→ Correct Error Reporting
→ Safe Recovery
→ User Experience
→ Convenience
```

Do not sacrifice data integrity just to make the operation appear successful.

---

# 85. Final Principle

The purpose of Error Handling is not to prevent errors from appearing.

The purpose is to make errors:

```text
Expected
→ Detectable
→ Understandable
→ Traceable
→ Recoverable when possible
→ Safe when recovery is impossible
```

The program must fail **safely and clearly** instead of apparently succeeding with wrong data or hiding the problem.

Final rule:

```text
Never hide an error.
Never silently lose data.
Never claim success when an operation failed.
Always preserve data integrity.
Always handle errors at the correct architectural layer.
