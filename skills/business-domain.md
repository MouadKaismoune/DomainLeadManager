---
name: business-domain
description: Defines the business domain, core entities, relationships, and Lead Generation workflow for a domain-investing lead management application.
---

# Business Domain Skill

## 1. Purpose

This skill defines the business concepts and relationships used by the application.

The application is designed specifically for domain investors who research potential companies that may be interested in acquiring a domain name.

The core business flow is:

Domain → Company → Contact → Email

The application helps the user organize this process and prepare high-quality leads for potential domain sales.

---

# 2. Core Business Concept

The application is based on a simple principle:

A domain name is an asset that may be valuable to one or more companies.

The user's task is to:

1. Identify a domain name.
2. Find companies that could benefit from that domain.
3. Identify relevant people inside those companies.
4. Find reliable contact information.
5. Organize the information into a structured lead.
6. Review the lead before outreach.
7. Export or use the lead for future sales activity.

The application does NOT automatically perform the entire sales process.

Its primary purpose is to organize research and lead information.

---

# 3. Domain

A `Domain` represents a domain name owned, controlled, or evaluated by the user.

Examples:

- example.com
- miamielectrician.com
- denverroofing.com
- austinplumbing.com

A domain is the starting point of the lead-generation process.

A domain may have:

- A domain name
- An extension
- A status
- Notes
- Creation date
- Last update date

Possible domain statuses:

- `active`
- `sold`
- `archived`

The application must treat the domain name as a distinct business entity.

A domain must not be confused with a company.

Example:

`denverroofing.com`

is a domain.

`Denver Roofing LLC`

is a company.

They are separate entities.

---

# 4. Company

A `Company` represents a business that may be a potential buyer of one or more domains.

Examples:

- Denver Roofing LLC
- Miami Electric Services
- Austin Plumbing Company

A company may have:

- Company name
- Website
- Description
- Address
- City
- State
- Country
- Company email addresses
- Company phone numbers
- Company social media accounts
- Contacts

A company can potentially be associated with multiple domains.

Example:

Company:

`ABC Roofing`

Potential domains:

- denverroofing.com
- denverroofers.com
- roofingdenver.com

Therefore, the company must be stored independently from the domain.

---

# 5. Domain → Company Relationship

The relationship between a domain and a company represents a potential sales opportunity.

This relationship is represented by a `Domain Lead`.

Example:

Domain:

`denverroofing.com`

Company:

`ABC Roofing`

Relationship:

`denverroofing.com → ABC Roofing`

This does NOT mean that the company has already expressed interest.

It means that the company has been identified as a potential prospect for the domain.

A company can be a lead for multiple domains.

A domain can also have multiple potential companies.

Example:

```text
denverroofing.com
    ├── ABC Roofing
    ├── Denver Roof Experts
    └── Rocky Mountain Roofing
````

And:

```text
ABC Roofing
    ├── denverroofing.com
    └── denverroofers.com
```

The application must support both situations.

---

# 6. Domain Lead

A `Domain Lead` represents the business relationship between a domain and a potential company.

It is one of the most important concepts in the application.

A Domain Lead contains information such as:

* Domain
* Company
* Lead status
* Priority
* Notes
* Creation date
* Last update date

Possible lead statuses:

* `new`
* `researching`
* `ready`
* `contacted`
* `interested`
* `not_interested`
* `archived`

Possible priorities:

* `low`
* `normal`
* `high`

The status belongs to the relationship between the domain and the company.

It should NOT be treated as a permanent property of the company.

For example:

```text
Company: ABC Roofing

Lead 1:
Domain: denverroofing.com
Status: interested

Lead 2:
Domain: roofingdenver.com
Status: not_interested
```

The same company can therefore have different lead statuses for different domains.

---

# 7. Contact

A `Contact` represents a specific person working at a company.

Examples:

* John Smith
* Sarah Johnson
* Michael Brown

A contact may contain:

* First name
* Last name
* Full name
* Job title
* Department
* Notes
* Contact emails
* Contact phone numbers
* Contact social accounts

A contact belongs to a company.

Example:

```text
Company:
ABC Roofing

Contacts:
├── John Smith
├── Sarah Johnson
└── Michael Brown
```

A contact must never be treated as a separate company.

The application must preserve the relationship:

```text
Company → Contact
```

---

# 8. Contact Relevance

Not every employee is equally useful for domain sales.

The application should allow the user to record the person's job title and department.

Examples of potentially relevant roles:

* Owner
* Founder
* CEO
* President
* Marketing Manager
* Marketing Director
* Business Development Manager
* Sales Manager

The application should store this information.

However, the application must NOT automatically assume that a specific job title is always the correct decision-maker.

The user remains responsible for evaluating contact relevance.

---

# 9. Email

The application supports two different types of email ownership.

## Company Email

A company email belongs directly to the business.

Examples:

* [info@example.com](mailto:info@example.com)
* [sales@example.com](mailto:sales@example.com)
* [support@example.com](mailto:support@example.com)

Relationship:

```text
Company → Company Email
```

A company can have multiple email addresses.

---

## Contact Email

A contact email belongs to a specific person.

Examples:

* [john@example.com](mailto:john@example.com)
* [sarah@example.com](mailto:sarah@example.com)

Relationship:

```text
Company → Contact → Contact Email
```

A contact email must belong to one person only.

It must never be silently assigned to multiple contacts.

---

# 10. Company Phone vs Contact Phone

The same ownership principle applies to phone numbers.

Company phone:

```text
Company → Company Phone
```

Example:

```text
+1 555 123 4567
```

Contact phone:

```text
Company → Contact → Contact Phone
```

Example:

```text
John Smith → +1 555 987 6543
```

The application must preserve the distinction between company-level information and person-level information.

---

# 11. Social Accounts

Social accounts can belong to either:

* A company
* A contact

Company social:

```text
Company → Social Account
```

Contact social:

```text
Company → Contact → Social Account
```

Examples of platforms:

* LinkedIn
* Facebook
* Instagram
* X
* Other

The application should store the platform and URL.

The application must not assume that every social account belongs to a person or every account belongs to a company.

---

# 12. Complete Business Relationship

The complete structure can be represented as:

```text
Domain
   │
   │ potential opportunity
   ▼
Company
   │
   ├── Company Emails
   ├── Company Phones
   ├── Company Socials
   │
   └── Contacts
          │
          ├── Contact Emails
          ├── Contact Phones
          └── Contact Socials
```

The domain and company are connected through:

```text
Domain Lead
```

Therefore:

```text
Domain
   │
   ▼
Domain Lead
   │
   ▼
Company
   │
   ▼
Contact
   │
   ▼
Email
```

This is the central business model of the application.

---

# 13. Lead Generation for Domain Trading

Lead Generation in this application means finding businesses that could potentially be interested in acquiring a specific domain.

The process is different from generic CRM lead generation.

The domain is the starting point.

The process is:

```text
Domain
    ↓
Potential Company
    ↓
Company Research
    ↓
Relevant Contact
    ↓
Contact Information
    ↓
Lead Review
    ↓
Outreach Preparation
```

The application should support this workflow without forcing the user into unnecessary CRM processes.

---

# 14. Step 1 — Identify the Domain

The user starts with a domain.

Example:

```text
denverroofing.com
```

The user evaluates what type of business could benefit from owning the domain.

The domain may indicate:

* Geographic location
* Industry
* Service
* Product
* Market

Example:

```text
denverroofing.com

Location:
Denver

Industry:
Roofing

Potential businesses:
Roofing companies operating in Denver
```

The application should store the domain independently before companies are added.

---

# 15. Step 2 — Find Potential Companies

The user researches companies that could have a commercial reason to acquire the domain.

For:

```text
denverroofing.com
```

possible prospects may include:

```text
ABC Roofing
Denver Roof Experts
Rocky Mountain Roofing
```

The user creates company records and associates them with the domain.

Each association becomes a Domain Lead.

---

# 16. Step 3 — Research the Company

The user researches each company to determine whether it is a reasonable prospect.

Useful information may include:

* Company name
* Website
* Location
* Industry
* Description
* Existing online presence
* Company email
* Company phone
* Social profiles
* Relevant employees

The application stores the information that the user discovers.

The application must not invent missing company information.

---

# 17. Step 4 — Find a Relevant Contact

After identifying a promising company, the user may search for a person who could be involved in purchasing or evaluating the domain.

Example:

```text
ABC Roofing
    ↓
John Smith
    ↓
Marketing Director
```

The contact is associated with the company.

The user may then add:

* Email
* Phone
* Social profile
* Job title
* Department
* Notes

---

# 18. Step 5 — Collect Contact Information

Contact information should be stored according to ownership.

Example:

```text
Company
├── info@abcroofing.com
├── sales@abcroofing.com
└── +1 555 111 2222

Contact: John Smith
├── john@abcroofing.com
├── +1 555 333 4444
└── LinkedIn URL
```

The application must preserve this distinction.

Do not move a company email into a person's record simply because it may be useful for outreach.

---

# 19. Step 6 — Review the Lead

Before considering a lead ready for outreach, the user should be able to review:

```text
Domain
Company
Website
Company information
Relevant contact
Contact role
Email
Phone
Social profiles
Notes
Lead status
Priority
```

The application should make this information easy to inspect.

The goal is to help the user determine:

> Is this company a good potential buyer for this domain?

---

# 20. Lead Status Meaning

The application uses statuses to represent the progress of a domain-company opportunity.

## new

The company has recently been identified as a potential lead.

```text
Domain → Company
Status: new
```

---

## researching

The user is currently investigating the company or gathering additional information.

---

## ready

The lead has enough useful information to be considered ready for outreach.

This does not mean that an email has been sent.

---

## contacted

The user has already contacted the company.

The application does not need to send the message itself in the first version.

---

## interested

The company has shown interest in the domain.

---

## not_interested

The company has been determined not to be interested.

---

## archived

The lead is no longer active but should remain in the database for historical reference.

---

# 21. Lead Priority

Priority helps the user organize prospects.

Available values:

```text
low
normal
high
```

Priority is a user-controlled organizational field.

The application must not automatically claim that a lead is high priority unless an explicit business rule is introduced later.

Priority is different from lead status.

Example:

```text
Status: researching
Priority: high
```

and:

```text
Status: ready
Priority: normal
```

are both valid.

---

# 22. Duplicate Detection

Duplicate detection is important because lead research can easily produce repeated companies, contacts, emails, phones, or social URLs.

The application follows three levels.

## Exact Duplicate

The system should prevent exact duplicates when the business rule requires uniqueness.

Examples:

* Same normalized domain
* Same normalized email
* Same domain-company relationship

---

## Strong Duplicate

The system should warn the user when a strong duplicate is detected.

Examples:

* Same website
* Same normalized phone
* Same social URL

The application should warn rather than silently delete or merge data.

---

## Possible Duplicate

The system may suggest possible duplicates when information appears similar.

Examples:

```text
ABC Roofing LLC
ABC Roofing

Denver Roof Experts
Denver Roofing Experts
```

Similarity does not prove that two records represent the same company.

The final decision belongs to the user.

The application must never automatically delete or merge records based only on similarity.

---

# 23. Data Normalization

Normalization is used to improve duplicate detection while preserving the original information for display.

Examples:

Email:

```text
John@Example.com
```

Normalized:

```text
john@example.com
```

Domain:

```text
Example.COM
```

Normalized:

```text
example.com
```

Website:

```text
https://www.example.com/
```

may be normalized for comparison.

The original value should remain available where appropriate.

Normalization is for comparison and integrity, not for destroying user-entered information.

---

# 24. Data Ownership Rules

The following ownership rules are fundamental:

```text
Domain
    └── Domain Lead
            └── Company
                    ├── Company Emails
                    ├── Company Phones
                    ├── Company Socials
                    └── Contacts
                            ├── Contact Emails
                            ├── Contact Phones
                            └── Contact Socials
```

Important rules:

1. A domain is independent from a company.
2. A company is independent from a domain.
3. A Domain Lead connects a domain to a company.
4. A contact belongs to one company.
5. A contact email belongs to one contact.
6. A company email belongs directly to a company.
7. Company-level information must not be confused with person-level information.
8. A company may be associated with multiple domains.
9. A domain may be associated with multiple companies.
10. Deleting a domain-company relationship must not automatically delete the company.

---

# 25. Data Preservation

The application is designed for research data.

Research information can be difficult to collect again.

Therefore:

* Do not silently delete useful data.
* Do not automatically merge companies.
* Do not automatically merge contacts.
* Do not overwrite existing contact information without an explicit action.
* Preserve notes.
* Preserve historical lead records when possible.
* Prefer archiving over destructive deletion when appropriate.

The user must remain in control of data changes.

---

# 26. What the Application Is NOT

This application is not intended to become a full CRM in the first version.

Do not introduce features such as:

* Email marketing campaigns
* Mass email sending
* Automated outreach
* Browser automation
* Web scraping
* AI lead scoring
* Complex sales pipelines
* Accounting
* Invoicing
* Inventory management
* Payment processing
* Complex marketing automation
* Advanced analytics
* Complex dashboards

unless explicitly requested later.

The application should remain focused on domain-investing lead research and organization.

---

# 27. Business Logic vs UI

Business concepts must not depend on the graphical interface.

For example:

The rule:

```text
A contact email belongs to one contact.
```

is a business rule.

It must not exist only inside a UI form.

Similarly:

```text
A domain-company pair represents one Domain Lead.
```

is a business rule and must be enforced at the appropriate business/data layers.

The UI should display and collect information.

The Service/Business layer should control business behavior.

The Repository layer should handle persistence.

---

# 28. Lead Generation Data Quality

Lead quality is more important than lead quantity.

A large number of poorly researched companies is less useful than a smaller number of relevant prospects.

The application should therefore make it easy to:

* Review company information
* Review contact information
* Verify email ownership
* Record sources
* Add notes
* Detect duplicates
* Mark lead status
* Assign priority
* Search and filter leads

The application should help the user maintain organized and trustworthy research data.

---

# 29. Source Tracking

Whenever contact information or company information comes from an external source, the application may store the source.

Examples:

```text
Google
Company Website
LinkedIn
Facebook
Business Directory
Manual Research
Other
```

The source is informational.

The application must not assume that information from a particular source is automatically accurate.

The user is responsible for verification.

---

# 30. Example Complete Lead

Example domain:

```text
denverroofing.com
```

Potential company:

```text
ABC Roofing LLC
```

Domain Lead:

```text
Domain:
denverroofing.com

Company:
ABC Roofing LLC

Status:
ready

Priority:
high
```

Company information:

```text
Website:
abcroofing.com

City:
Denver

Country:
United States
```

Company email:

```text
info@abcroofing.com
```

Contact:

```text
John Smith

Job Title:
Marketing Director
```

Contact email:

```text
john@abcroofing.com
```

Contact phone:

```text
+1 555 123 4567
```

The complete relationship becomes:

```text
denverroofing.com
        │
        ▼
    Domain Lead
        │
        ▼
 ABC Roofing LLC
        │
        ├── info@abcroofing.com
        │
        └── John Smith
                │
                ├── Marketing Director
                ├── john@abcroofing.com
                └── +1 555 123 4567
```

This is a valid lead record.

---

# 31. Important Distinction: Company vs Contact

Codex must never treat the following as interchangeable:

```text
Company
Contact
```

For example:

```text
ABC Roofing
```

is a company.

```text
John Smith
```

is a contact.

The company may have:

```text
info@abcroofing.com
```

while John may have:

```text
john@abcroofing.com
```

These must remain separate records.

This distinction is fundamental to the application's business domain.

---

# 32. Important Distinction: Domain vs Lead

A domain is an asset.

A lead is an opportunity involving that asset and a potential buyer.

Therefore:

```text
Domain ≠ Lead
```

Example:

```text
denverroofing.com
```

can exist without any companies.

Once the user identifies:

```text
ABC Roofing
```

as a potential buyer, the relationship becomes:

```text
denverroofing.com → ABC Roofing
```

which is a Domain Lead.

---

# 33. Important Distinction: Lead vs Contact

A contact is a person.

A lead represents a potential business opportunity.

Therefore:

```text
Lead ≠ Contact
```

A lead may have zero contacts while research is incomplete.

Example:

```text
denverroofing.com
        ↓
ABC Roofing
        ↓
No contact found yet
```

This is still a valid lead.

Later:

```text
ABC Roofing
        ↓
John Smith
        ↓
john@abcroofing.com
```

The lead becomes more complete.

---

# 34. Recommended Mental Model

Codex should understand the application using the following mental model:

```text
DOMAIN
"What am I trying to sell?"

        ↓

COMPANY
"Who could potentially want it?"

        ↓

CONTACT
"Who inside that company may be relevant?"

        ↓

EMAIL / PHONE / SOCIAL
"How can the relevant business/person be contacted?"

        ↓

LEAD STATUS
"What is the current state of this opportunity?"
```

This mental model should guide implementation decisions throughout the project.

---

# 35. Business Domain Decision Rule

When implementing a feature, Codex must first determine which business entity the feature belongs to.

Ask:

1. Is this information about the domain itself?
2. Is this information about the company?
3. Is this information about a relationship between a domain and company?
4. Is this information about a person?
5. Is this information about contact information?
6. Is this information about lead progress?

Do not place data in another entity simply because it is convenient.

The business meaning of the data must determine where it belongs.

---

# 36. Final Business Domain Principle

The entire application is centered around one simple business workflow:

```text
Find a valuable domain
        ↓
Find companies that could benefit from it
        ↓
Research those companies
        ↓
Find relevant contacts
        ↓
Collect reliable contact information
        ↓
Organize the information
        ↓
Review the lead
        ↓
Prepare for potential outreach
```

The application exists to make this process organized, reliable, and easy to manage.

Every future feature must support this core purpose.

If a proposed feature does not clearly improve domain research, company identification, contact organization, lead management, data quality, or outreach preparation, it should not be added without explicit approval.
