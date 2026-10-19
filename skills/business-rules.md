---
name: business-rules
description: Defines the core business rules for the lead generation application including companies, domains, contacts, emails, duplicate detection, and lead management.
---

# Business Rules Skill

## Purpose

This skill defines the fundamental business rules for the Lead Generation Application.

Codex must consider these rules as an essential part of the program logic.

When creating or modifying:

- Models
- Services
- Repositories
- Collectors
- Parsers
- Validators
- Duplicate Detection
- Lead Management
- Database Operations
- UI Actions

Must ensure the change does not violate these rules.

This skill describes **the application's business domain rules**, not just technical database rules.

---

# 1. Core Concepts

The application relies on a set of main entities:

```text
Company
    ↓
Domain
    ↓
Contact
    ↓
Email
    ↓
Lead
```

But these entities are not necessarily linked in a 1:1 relationship.

Must always respect the relationships defined in this skill.

---

# 2. Company

`Company` represents a real company or organization.

Each company must have an independent record.

Must not create a new company just because of finding:

* New Domain.
* New Contact.
* New Email.
* New Lead.

If data points to the same company, must link to existing record instead of creating duplicate Company.

---

# 3. Company Can Be Associated with Multiple Domains

The relationship between Company and Domain allows a company to own more than one Domain.

Example:

```text
Company A
    ├── example.com
    ├── example.net
    └── example.org
```

Do not assume:

```text
1 Company = 1 Domain
```

---

# 4. Domain Is Not a Company

Existence of a Domain does not automatically mean it represents an independent company.

Example:

```text
example.com
example.net
example.org
```

Can all belong to:

```text
Company A
```

Therefore must not create a new Company for each Domain.

---

# 5. Domain Detection

When finding a new Domain:

1. Normalize the Domain.
2. Check for its existence.
3. Try to identify associated company.
4. If company is known, link Domain to it.
5. If Domain already exists, do not create matching copy.
6. If Domain-company relationship is uncertain, do not link definitively without sufficient evidence.

---

# 6. Domain Normalization

Before comparing Domains, must unify their form as much as possible.

Must handle formal differences like:

```text
https://example.com
http://example.com
www.example.com
example.com/
```

Per project rules.

Must not remove parts of Domain if it could change its true identity.

Goal is to reach a Canonical Representation suitable for comparison.

---

# 7. Contact

`Contact` represents a person associated with a company.

Example:

```text
Company A
    ├── John Smith
    ├── Sarah Jones
    └── David Brown
```

A company can contain multiple Contacts.

---

# 8. Contact Is Not Necessarily a Lead

Existence of a Contact does not automatically mean it's a Lead.

A Contact may be:

* Found.
* Data verified.
* Present in database.
* But not yet converted to a business opportunity.

Therefore must not automatically create Lead just because a Contact was created.

---

# 9. Personal Email

Personal email represents an email linked to a specific person.

Example:

```text
john@example.com
```

If confirmed that a personal email belongs to a specific person, must not link the same personal email to multiple different people.

Rule:

> Confirmed personal email belongs to one person only.

---

# 10. Don't Assume Email Ownership

If a personal email is found and its owner cannot be confirmed, do not automatically assign it to a person just because of name similarity.

Example:

```text
john@example.com
```

Does not automatically mean its owner is:

```text
John Smith
```

Unless there is appropriate evidence.

---

# 11. Generic Email

Company generic email differs from personal email.

Examples:

```text
info@example.com
sales@example.com
contact@example.com
support@example.com
```

Generic email can be associated with the company, not a specific person.

Must not create a fake Contact for every generic email.

---

# 12. Email Types

Must distinguish between:

```text
Personal Email
Generic / Company Email
Unknown
```

And must not consider every discovered email as a personal email.

---

# 13. Don't Delete Data When Source Differs

If same company or person is found from a different source, do not delete old record just because new source has different data.

Must compare data first.

New source may be:

* More accurate.
* Newer.
* Incomplete.
* Different in some fields.

Data is not automatically replaced without a clear rule.

---

# 14. Duplicate Detection

Duplicate Detection is the process of discovering records that **may represent the same entity**.

Must distinguish between:

```text
Confirmed Duplicate
Possible Duplicate
Not Duplicate
```

---

# 15. No Automatic Merge

This is a fundamental rule:

> Do not merge Duplicate Records automatically.

Even if similarity score is high, must not permanently merge records without appropriate confirmation.

Example:

```text
ABC Solutions
ABC Solution
```

May be the same company, but must not merge automatically just due to textual similarity.

---

# 16. No Automatic Deletion

Do not delete a record considered Duplicate automatically.

Instead of:

```text
Duplicate detected
        ↓
Delete
```

Path must be:

```text
Duplicate detected
        ↓
Mark / Flag
        ↓
Review
        ↓
User Decision
        ↓
Merge / Keep Both / Ignore
```

---

# 17. Duplicate Detection Must Be Non-Destructive

Duplicate detection process must not by itself lead to:

* Deleting data.
* Merging data.
* Changing data ownership.
* Losing Source Information.

Detection function is **discovery and flagging**.

Merge or deletion decision is a separate process.

---

# 18. Exact Duplicate

If there is a confirmed match per a strong rule, record can be classified as:

```text
Exact Duplicate
```

But even in this case:

> Detection does not mean Delete.

Must retain data until the case is processed per Business Rules.

---

# 19. Possible Duplicate

If data is similar but there's insufficient evidence, must classify as:

```text
Possible Duplicate
```

And must not treat it as Confirmed Duplicate.

Example:

```text
Acme Plumbing LLC
Acme Plumbing
```

Similarity alone is not enough.

---

# 20. Duplicate Matching

Can use multiple indicators when detecting duplicates.

For Company:

```text
Domain
Website
Company Name
Phone
Address
Location
```

For Contact:

```text
Email
Name
Company
Job Title
```

For Email:

```text
Normalized Email
```

Must not rely on a single indicator blindly when error probability is high.

---

# 21. Matching Indicator Priority

Generally:

```text
Strong Identifier
      ↓
Exact Match
      ↓
Multiple Matching Signals
      ↓
Similarity
      ↓
Possible Duplicate
```

Stronger evidence means higher confidence.

But must not convert textual similarity alone into a Confirmed Match.

---

# 22. Duplicate Score

If program uses a system to measure duplication probability, must consider it:

```text
Detection Signal
```

Not a final decision.

Example:

```text
Score = 95%
```

Does not mean:

```text
Delete Automatically
```

But:

```text
Very Likely Duplicate
→ Review
```

---

# 23. Retain Data Source

When detecting Duplicate from a new source, do not lose source information.

Must be possible to know:

```text
Where was this data found?
When was it found?
What source produced it?
```

Because data source may be important during review or merge.

---

# 24. Merge

If Merge operation is allowed in future, it must be an independent and clear process.

Before merging must determine:

```text
Primary Record
Secondary Record
```

Then determine how to handle:

* Different fields.
* Contacts.
* Domains.
* Emails.
* Sources.
* Data history.
* Relationships.
* Dependent records.

Do not perform a simple Merge like:

```text
UPDATE primary
DELETE secondary
```

Without analyzing relationships and dependent data.

---

# 25. Lead

`Lead` represents an opportunity or contact with potential commercial value.

Not every:

```text
Company
Contact
Email
```

Is necessarily a Lead.

Must have clear rules determining when data becomes a Lead.

---

# 26. Lead Statuses (Canonical List)

> **📌 Canonical Source of Truth:**
> The Lead Status values for this project are defined in `project-overview.md`
> (Section 13). This section restates them for convenience and adds operational rules.
> If there's any conflict, the list in `project-overview.md` wins.

System must use these clear Lead statuses:

```text
new
researching
ready
contacted
interested
not_interested
archived
```

**Important:**
- Do NOT use generic CRM statuses such as `Qualified`, `Negotiating`, `Won`, `Lost` unless the user explicitly requests them.
- These 7 statuses are tailored to the domain-investing lead research workflow.
- All Services, Repositories, UI, and Tests must use this exact list.

---

# 27. new

Means:

> Lead was created or added to system, but not yet processed.

Example:

```text
new Lead
```

Does not mean the company is interested or a good fit.

---

# 28. researching

Means:

> The user is currently investigating the company or gathering additional information.

Examples of research activity:

* Searching for company website.
* Looking up decision-makers.
* Verifying company legitimacy.
* Collecting contact information.

---

# 29. ready

Means:

> The lead has enough useful information to be considered ready for outreach.

This does not mean an email has been sent.

The user has confirmed:
* Company is real and relevant.
* At least one contact is available.
* The domain is a reasonable fit.

---

# 30. contacted

Means:

> The user has already contacted the company.

Such as:

* Sending Email.
* Making a call.
* Manual outreach.

Does not mean the company responded or showed interest.

---

# 31. interested

Means:

> The company has shown clear interest in the domain.

Must not put Lead in this state just because a message was sent.

Must have evidence of interest (e.g., reply, phone call, explicit expression of interest).

---

# 32. not_interested

Means:

> The company has been determined not to be interested.

Examples:

* Explicit rejection.
* No need for the domain.
* Already has a similar domain.
* Out of target market.

If system supports reasons, must store reason instead of just status.

---

# 33. archived

Means:

> The Lead is no longer active in current workflow, but its data must be retained.

Examples:

* Too old to contact.
* Domain sold elsewhere.
* Company went out of business.
* User decided not to pursue.

Archive is NOT the same as Delete.

---

# 34. Don't Delete Lead When Archived or not_interested

Important rule:

```text
archived ≠ Deleted
not_interested ≠ Deleted
```

If a Lead is archived or marked as not_interested, it is not automatically deleted.

Must retain history and data for review and analysis purposes.

---

# 35. Lead Transitions

Status transitions must be logical.

Typical path:

```text
new
  ↓
researching
  ↓
ready
  ↓
contacted
  ↓
interested
```

Or alternative ending:

```text
new
  ↓
researching
  ↓
ready
  ↓
contacted
  ↓
not_interested
  ↓
archived
```

But application must not assume every Lead will pass through all statuses.

Skipping statuses (e.g., going directly from `new` to `contacted`) is allowed when justified by the data.

---

# 36. Reopening Lead

A Lead that was:

```text
archived
```

or:

```text
not_interested
```

May become active again if a new opportunity appears.

If allowed in Business Rules, must record the change instead of deleting previous history.

---

# 37. Lead Status ≠ Data Quality

Must not confuse:

```text
Lead Status
```

And:

```text
Data Quality
```

Example:

```text
Lead Status = contacted
Data Quality = Low
```

Both are different concepts.

Lead Status describes the commercial/progress stage.

Data Quality describes the reliability and completeness of the data.

---

# 38. Lead Status ≠ Email Status

Must not use Lead status to express email status.

Example:

```text
Lead Status:
ready

Email Status:
Unverified
```

These are two independent states.

---

# 40. Don't Create Duplicate Lead

If same business opportunity already exists, do not create new Lead just because same company or Contact found from another source.

Must first check for existing Lead linked to same entity or same opportunity.

---

# 41. Multiple Domains and Leads

Multiple Domains for a company does not automatically mean creating multiple Leads.

Example:

```text
Company A
  ├── domain1.com
  ├── domain2.com
  └── domain3.com
```

These can all be linked to the same company and business opportunity.

Do not create a Lead for each Domain without a clear business reason.

---

# 42. Multiple Contacts and Leads

Multiple Contacts in same company does not necessarily mean creating independent Lead for each person.

Must depend on Lead concept in system.

If Lead represents:

```text
Company Opportunity
```

Then company may be the basis of Lead.

But if it represents:

```text
Person / Contact Opportunity
```

Then Contact may be a fundamental part of Lead.

Must not mix the two models.

---

# 43. Source Data Doesn't Become Absolute Truth

Data extracted from external sources is not automatically correct.

Must consider it:

```text
Collected Data
```

Then pass through:

```text
Normalization
Validation
Duplicate Detection
```

Before considering it reliable data.

---

# 44. Don't Overwrite Good Data Automatically

If database contains reliable data, and new less complete data arrives, do not automatically replace old data.

Example:

Database:

```text
phone = 0555000000
website = example.com
```

New source:

```text
phone = NULL
website = example.com
```

Import must not lead to:

```text
phone = NULL
```

Data loss is unacceptable unless change is intentional.

---

# 45. New and Additional Data

If new source contains additional information not present, can use it to enrich record.

Example:

Current record:

```text
Company
Website
```

New source:

```text
Company
Website
Phone
```

Can add:

```text
Phone
```

Instead of creating new Company.

---

# 46. Conflict Resolution

If two sources differ on same information, do not pick a random value.

Must have clear logic like:

```text
Trusted Source
    ↓
More Recent Data
    ↓
Verified Data
    ↓
Existing Data
```

But final priority order must follow project rules and its sources.

---

# 47. Manual Review

When data is uncertain, must use a status or Queue for manual review instead of making a destructive decision.

Examples:

```text
Possible Duplicate
Conflicting Data
Uncertain Company Match
Uncertain Contact Match
```

---

# 48. No Data Loss Due to Automation

Automation must help the user, not make destructive decisions without review possibility.

Especially in:

* Merge.
* Delete.
* Duplicate Resolution.
* Contact Assignment.
* Company Assignment.

---

# 49. Deletion Rule

Automatic deletion is forbidden in the following cases unless an explicit rule exists:

```text
Duplicate Detection
Failed Validation
Low Quality Lead
Archived Lead
Old Lead
Different Source
Missing Information
```

Having a data problem does not mean data must be deleted.

---

# 50. Database Is Not the Sole Business Decision Source

Database Constraints protect data, but don't alone determine Business Logic.

Example:

```text
UNIQUE(email)
```

May prevent technical duplication, but doesn't determine:

* Is email personal?
* Is email generic?
* Does it belong to a Contact?
* Should it be linked to a Company?
* Is the data reliable?

These are Business Logic decisions.

---

# 51. Priority Rule

When conflict exists between:

```text
Convenience
```

And:

```text
Data Integrity
```

Must prioritize:

```text
Data Integrity
```

And when conflict exists between:

```text
Automation
```

And:

```text
Data Safety
```

Must prioritize:

```text
Data Safety
```

---

# 52. General Data Workflow

General data path must be close to:

```text
External Source
      ↓
Collection
      ↓
Raw Data
      ↓
Normalization
      ↓
Parsing
      ↓
Validation
      ↓
Duplicate Detection
      ↓
Review if Needed
      ↓
Create / Update Entity
      ↓
Create / Update Lead
```

Must not jump directly from:

```text
External Source
```

To:

```text
Database
```

Without passing through necessary operations.

---

# 53. History Preservation Rule

Business data may change over time.

Must not destroy previous history without reason.

Especially:

* Lead Status.
* Source.
* Contact Information.
* Domain Relationships.
* Duplicate Decisions.
* Merge Decisions.

If system needs History, must design it explicitly instead of overwriting data and losing history.

---

# 54. No Assumption Rule

When insufficient information exists, Codex must not assume:

```text
Same Name = Same Company
Same Domain = Same Person
Same Email Pattern = Same Contact
Similar Company Name = Duplicate
New Source = Better Data
```

Must rely on evidence and rules.

---

# 55. Forbidden Rules

Codex is prohibited from implementing the following behaviors without request or explicit rule:

```text
Automatic Duplicate Merge
Automatic Duplicate Delete
Automatic Company Creation for Every Domain
Automatic Lead Creation for Every Contact
Automatic Contact Creation for Every Generic Email
Automatic Contact Assignment Without Evidence
Automatic Replacement of Existing Data
Automatic Deletion of Archived Leads
Automatic Deletion of Invalid Records
```

---

# 56. Checklist Before Any New Business Logic

Before adding new logic, Codex must verify:

* [ ] What entity does the code deal with?
* [ ] Can Company contain multiple Domains?
* [ ] Is Contact linked to a valid Company?
* [ ] Is email Personal or Generic?
* [ ] Is personal email attributed to a confirmed person?
* [ ] Is data duplicated?
* [ ] Is duplication Confirmed or Possible?
* [ ] Should we only Flag the duplication?
* [ ] Is there a risk of data loss?
* [ ] Does the process affect Lead?
* [ ] What is the current Lead status?
* [ ] Is the status transition logical?
* [ ] Does the process create a duplicate Lead?
* [ ] Is there a data source that must be retained?
* [ ] Does the case need manual review?

---

# Final Principle

The program must handle data as real data that may contain:

```text
Duplicates
Conflicts
Missing Data
Multiple Sources
Multiple Domains
Multiple Contacts
Multiple Emails
Uncertain Matches
```

Therefore the system must be:

```text
Conservative
Non-destructive
Traceable
Reviewable
Data-safe
```

Most important rule:

> When the system is not certain that two records represent the same entity, it must consider them "Possible Duplicate" and preserve both records instead of automatically merging or deleting.

Second rule:

> Duplicate detection is an analytical decision, while merge and deletion are separate operations requiring a clear decision.

Third rule:

> Automation must not lead to loss of valid data just because new data is incomplete or conflicting.
