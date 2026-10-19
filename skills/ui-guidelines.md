---
name: ui-guidelines
description: Defines visual and functional rules for the Lead Generation Application interface, focusing on simplicity, clarity, and functionality with clear rules preventing unnecessary dashboards, charts, and visual complexity.
---

# UI Guidelines Skill

## Purpose

This skill defines the visual and functional rules for the Lead Generation Application interface.

The goal is to build an interface that is:

- Simple.
- Professional.
- Clear.
- Fast to use.
- Easy to learn.
- Organized.
- Extensible.
- Free of unnecessary visual elements or functions.

Codex must consider these rules a fundamental reference when creating or modifying any part of the user interface.

---

# 1. Fundamental Principle

The interface must help the user accomplish work, not showcase data.

Priority is:

```text
Clarity
↓
Usability
↓
Efficiency
↓
Consistency
↓
Visual Polish
```

And NOT:

```text
Animations
+
Charts
+
Cards
+
Decorations
```

---

# 2. Simplicity First

The interface must be as simple as possible.

Do not add an element to the interface unless it has a clear benefit for the user.

Before adding any:

* Card.
* Button.
* Chart.
* Widget.
* Animation.
* Statistic.
* Section.

Ask:

> Does the user actually need this element to accomplish the task?

If the answer is no, do not add it.

---

# 3. No Unnecessary Dashboard

Do not create a Dashboard full of statistics just because the application needs a main page.

Must avoid a Dashboard containing:

```text
Total Leads
Total Companies
Conversion Rate
Lead Score
Revenue
Growth
Charts
Graphs
Activity Metrics
```

If this information is not actually necessary in the user's workflow.

---

# 4. No Unnecessary Charts

Do not add:

* Pie Charts.
* Bar Charts.
* Line Charts.
* Area Charts.
* Donut Charts.

Unless there's an actual need to make a decision through them.

If the information can be displayed in:

```text
Table
List
Number
Status
Filter
```

Then the simpler form is better.

---

# 5. No Decorative Statistics

Do not use large numbers inside Cards just to make the page look professional.

Unwanted example:

```text
┌────────────┐
│ 12,450      │
│ Total Leads │
└────────────┘
```

If the number doesn't help the user take an action.

---

# 6. Home Page

The home page must help the user quickly access the most important operations.

Can contain:

* Clear Navigation.
* Shortcuts to important operations.
* Latest data or important tasks.
* Current data collection status.
* Quick actions.

But must not turn it into a complex analytical Dashboard.

---

# 7. Navigation

Navigation must be clear and fixed.

Prefer using a fixed main Navigation, like:

```text
Leads
Companies
Contacts
Domains
Collection
Sources
Settings
```

Can modify names per actual project structure.

Essential element locations must not change between pages without reason.

---

# 8. Navigation Ordering

Must order Navigation elements by usage importance, not by the order of programmatic module creation.

Most used elements must be easily accessible.

Example:

```text
Leads
Companies
Contacts
Domains
Collection
Settings
```

If a new module is added, must determine its place logically instead of putting it randomly in the list.

---

# 9. Don't Overdo Navigation

Do not make the sidebar contain dozens of elements.

If the number of elements becomes large, use:

* Grouping.
* Sections.
* Sub-navigation.

Instead of creating a long, unclear list.

---

# 10. Navigation Hierarchy

The user must always know:

```text
Where am I?
Where did I come from?
Where can I go?
```

Can use:

* Page title.
* Breadcrumb when needed.
* Navigation state.
* Tabs when needed.

But do not use all of them at once if not necessary.

---

# 11. Page Structure

Every page must have a clear structure.

Preferred pattern:

```text
Page
│
├── Header
│   ├── Title
│   └── Primary Action
│
├── Filters / Search
│
├── Main Content
│
└── Pagination / Secondary Actions
```

The page must not be a random collection of elements.

---

# 12. Page Header

The page Header must contain:

* Clear title.
* Short description when needed.
* The primary action for the page.

Example:

```text
Leads

Manage and review collected leads.

[ + Add Lead ]
```

Do not add a long description if not necessary.

---

# 13. Primary Action

Every page must have a clear primary action when appropriate.

Examples:

```text
Leads
→ Add Lead

Companies
→ Add Company

Collection
→ Start Collection

Domains
→ Add Domain
```

The page must not contain a large number of buttons with the same visual importance.

---

# 14. Secondary Actions

Secondary actions must be less prominent than the primary action.

Like:

```text
Edit
Delete
Export
Import
Refresh
```

Do not make all buttons Primary Buttons.

---

# 15. Buttons

Buttons must be:

* Clear.
* Short.
* Direct action.
* Consistent.

Use:

```text
Add Lead
Save
Cancel
Edit
Delete
Export
Start Collection
Stop
```

Instead of long texts inside buttons.

---

# 16. Destructive Actions

Dangerous actions like:

```text
Delete
Remove
Clear
Reset
```

Must be clear and distinct from normal actions.

When needed, must show a Confirmation Dialog before execution.

---

# 17. Delete Confirmation

Do not use a Confirmation Dialog for every simple action.

Use it when the action is:

* Destructive.
* Hard to undo.
* May lead to data loss.

Example:

```text
Delete this lead?

This action cannot be undone.

[Cancel] [Delete]
```

---

# 18. Tables

Tables are a fundamental element in the Lead Generation program.

Must be:

* Clear.
* Easy to read.
* Searchable.
* Filterable.
* Sortable when needed.

Do not display dozens of columns at once if not necessary.

---

# 19. Table Columns

Must display the most important information first.

Example for Leads table:

```text
Company
Contact
Email
Domain
Status
Source
Actions
```

Do not automatically add all columns existing in the database to the interface.

---

# 20. Table Actions

Basic actions can be:

```text
View
Edit
Delete
```

And must avoid putting a large number of icons inside each row.

If there are many actions, use:

```text
More
```

Or an Actions list.

---

# 21. Empty States

When there's no data, do not just display an empty table.

Show a clear message.

Example:

```text
No leads yet.

Start collecting leads or add one manually.

[ Start Collection ]
```

The Empty State must tell the user:

* What happened?
* Why is there no data?
* What can they do?

---

# 22. Loading States

When executing an operation that takes time:

* Show a Loading State.
* Do not make the user think the application has stopped.
* Disable actions that cannot be executed during the operation if necessary.

Example:

```text
Collecting leads...
```

With appropriate Progress if the operation allows it.

---

# 23. Progress

Data collection operations may take time.

When it's possible to know the progress, can display:

```text
Collecting...
127 / 500
```

Or a Progress Bar.

But do not use fake Progress if the program doesn't know the real percentage.

---

# 24. Collection Interface

The lead collection interface must be clear and direct.

Prefer organizing it into:

```text
Collection Settings
        ↓
Source / Input
        ↓
Collection Options
        ↓
Start
        ↓
Progress
        ↓
Results
```

Do not put dozens of options on the main screen.

---

# 25. Collection Controls

Control elements related to data collection must be clear.

Like:

```text
Source
Keyword
Location
Limit
Start
Pause
Stop
```

Do not use ambiguous Labels.

---

# 26. Collection Status

The collection process status must be clear.

Examples:

```text
Idle
Running
Paused
Completed
Failed
Stopped
```

Can use colors or Badges in a limited way to distinguish states.

---

# 27. Lead Status

Must display Lead status in a clear way.

Example (canonical Lead Statuses):

```text
new
researching
ready
contacted
interested
not_interested
archived
```

Prefer using a Badge or clear Label instead of displaying the status as an internal number.

---

# 28. Status Consistency

Must use the same appearance for the same status throughout the application.

If:

```text
ready
```

Appears as a Badge on the Leads page, do not make it a Button on another page without reason.

---

# 29. Search

Search is a fundamental element in the program.

Must place the Search Box in a clear place when the page contains a large number of records.

Example:

```text
Search leads...
```

The Placeholder must be clear about what can be searched for.

---

# 30. Filters

Use Filters when the amount of data is large or when filtering is important for the workflow.

Examples:

```text
Status
Source
Country
Industry
Verification Status
```

Do not add dozens of Filters in the main interface.

Can put advanced options in:

```text
Advanced Filters
```

---

# 31. Search + Filters

When Search and Filters exist together, the relationship between them must be clear.

Example:

```text
[ Search leads... ]

Status: [ All ]
Source: [ All ]
Country: [ All ]

[ Reset Filters ]
```

---

# 32. Forms

Forms must be:

* Short.
* Organized.
* Logically divided.
* Easy to understand.

Do not display all possible fields to the user if not necessary.

---

# 33. Required Fields

Must clarify required fields.

Do not make the user discover after pressing Save that several fields are missing without clarification.

---

# 34. Validation Messages

Error messages must be:

* Clear.
* Short.
* Linked to the field.
* Useful for the user.

Bad:

```text
Invalid input.
```

Better:

```text
Enter a valid email address.
```

---

# 35. Forms Do Not Contain Business Logic

UI Form is responsible for:

* Data input.
* Displaying Validation Errors.
* Sending data to Service.

Must not contain complex Business Logic.

Path:

```text
Form
  ↓
Service
  ↓
Validation / Business Rules
  ↓
Repository
```

---

# 36. Detail Pages

When displaying Company, Lead, or Contact details, must organize information into logical Sections.

Example:

```text
Company Details
────────────────
Basic Information

Domains
────────────────
...

Contacts
────────────────
...

Leads
────────────────
...
```

Do not display all data in a single block.

---

# 37. Related Data

When displaying a Company, can show related data like:

```text
Domains
Contacts
Leads
Sources
```

But must not repeat the same data in multiple Sections without need.

---

# 38. Visual Hierarchy

Must have a clear difference between:

```text
Page Title
Section Title
Body Text
Secondary Text
Button
Status
```

Use:

* Size.
* Weight.
* Spacing.
* Borders.
* Backgrounds.

To build a clear Hierarchy.

---

# 39. Spacing

Use a consistent spacing system.

Do not make every Component use a different random Padding.

Distances must look:

```text
Consistent
Predictable
Balanced
```

---

# 40. Typography

Use a limited number of font sizes and weights.

Avoid:

* Dozens of font sizes.
* Decorative fonts.
* Very small text.
* Heavy text everywhere.

Priority for clarity and readability.

---

# 41. Colors

Use a limited, consistent color system.

Prefer having:

```text
Primary
Background
Surface
Text
Secondary Text
Border
Success
Warning
Error
```

Do not use many colors just to make the interface look more lively.

---

# 42. Status Colors

Can use status colors, but color must not be the only way to understand the status.

Example:

```text
● ready
● contacted
● interested
```

The status name must also be written.

---

# 43. Icons

Use icons when they help understand the function.

Appropriate examples:

```text
Search
Edit
Delete
Settings
Refresh
Export
Import
```

Do not use Icons just for decoration.

---

# 44. Icon Buttons

If a button contains only an Icon, its meaning must be clear.

Use Tooltip when needed.

Do not use ambiguous icons for important functions.

---

# 45. Cards

Can use Cards when they help group related information.

But do not use a Card for everything.

Avoid:

```text
Card inside Card inside Card
```

Especially on data pages and tables.

---

# 46. Modals

Use Modal when the operation is:

* Short.
* Focused.
* Doesn't need a full page.

Examples:

```text
Add Lead
Confirm Delete
Import Data
```

Do not put a complete, complex Workflow inside a Modal.

---

# 47. Tabs

Can use Tabs when there are clear groups of related information.

Example:

```text
Company
├── Overview
├── Domains
├── Contacts
└── Leads
```

But do not use Tabs just to split a small page.

---

# 48. Responsive Layout

If the technology used supports window resizing, the interface must adapt to different sizes.

Do not depend on:

* Fixed Positions without need.
* Fixed Sizes that lead to content clipping.
* Elements that cannot be resized.

---

# 49. Accessibility

Must consider:

* Text clarity.
* Appropriate contrast.
* Readable font size.
* Not relying on color alone.
* Easy access to important elements.

---

# 50. Feedback

After important operations, must give the user clear Feedback.

Examples:

```text
Lead saved successfully.
Company updated successfully.
Collection completed.
Export completed.
```

Success messages must not be annoying or exaggerated.

---

# 51. Error Feedback

When an operation fails:

```text
Operation failed.
```

Is not always enough.

Must provide the most useful message possible.

Example:

```text
Unable to save the lead because the email already exists.
```

If the technical error is not appropriate for the user, do not display the Stack Trace inside the interface.

---

# 52. Notifications

Use Notifications or Toasts in moderation.

Do not show a notification for every small operation.

Notifications must be:

* Short.
* Understandable.
* Non-intrusive.

---

# 53. Animations

Do not use Animations excessively.

Can use a simple Animation when:

* It helps understand the transition.
* It gives Feedback.
* It makes the operation smoother.

But do not use Animation just for decoration.

---

# 54. Don't Use Dashboard as Default Solution

When adding a new Module, do not assume the user needs a Dashboard.

The correct question is:

> What task does the user want to perform?

Then design the interface around the task.

---

# 55. Don't Add Analytics Without Need

Do not add:

```text
Charts
Analytics
KPIs
Reports
Trends
Growth Graphs
```

Unless required by Business Requirements.

The core program's goal is collecting, organizing, and managing leads, not building an advanced Analytics platform.

---

# 56. Don't Add Visual Features on Your Own

Codex is prohibited from adding:

* New Dashboard.
* Chart.
* Analytics Section.
* KPI Cards.
* Animated Background.
* Decorative Illustrations.
* Complex Widgets.

Just to improve the appearance.

If there's a visual suggestion that might change the interface structure, it must be justified by a clear functional requirement.

---

# 57. Consistency

All pages must share:

```text
Navigation
Typography
Spacing
Buttons
Inputs
Tables
Badges
Dialogs
Colors
```

Do not design every page with a different style.

---

# 58. Reusable Components

If a Component repeats across multiple pages, must consider making it Reusable.

Examples:

```text
SearchBar
DataTable
StatusBadge
FilterPanel
ConfirmDialog
EmptyState
LoadingState
Pagination
```

This reduces:

* Code duplication.
* Design differences.
* Interface errors.

---

# 59. Don't Reinvent Components

Before creating a new Component, check for a similar existing one.

If the existing one is reusable, use it instead of creating a second copy.

---

# 60. Design Before Code Rule

Before significantly modifying UI:

1. Understand the current page.
2. Understand its function.
3. Identify the user who will use it.
4. Identify the core task.
5. Preserve the current structure if it's good.
6. Improve only the part that needs improvement.

Do not redesign the entire application for a small modification.

---

# 61. No Unnecessary Change Rule

If a Component works well, do not change it just to change the design.

Every UI modification must have a clear reason, such as:

* Improving usability.
* Solving a problem.
* Improving clarity.
* Unifying design.
* Supporting a new function.

---

# 62. Mobile / Desktop Rule

This application is Desktop-oriented.

Must prioritize:

```text
Desktop Usability
```

While maintaining interface flexibility when resizing the window if the technology supports it.

Do not sacrifice Desktop ease of use for an unneeded Mobile design.

---

# 63. Database Must Not Show to the User

Do not display technical table or column names to the end user.

Instead of:

```text
company_id
created_at
verification_status
```

Use understandable Labels:

```text
Company
Created
Verification Status
```

---

# 64. Terminology

Must use consistent terminology in the interface.

If using:

```text
Lead
Company
Contact
Domain
Email
Source
```

Must not randomly change them to other terms on different pages.

---

# 65. Language

If the application supports more than one language, must not write texts directly inside interface components in a way that prevents later translation.

Prefer putting translatable texts in an appropriate Translation system.

---

# 66. Text Rule

Texts must be:

* Short.
* Clear.
* Direct.
* Free of unnecessary technical terms.

Example:

```text
Start Collection
```

Better than:

```text
Execute Lead Data Collection Process
```

---

# 67. Large Tables Rule

When dealing with thousands of Leads, do not try to display all data at once.

Use when needed:

* Pagination.
* Lazy Loading.
* Filtering.
* Search.
* Sorting.

The interface must be usable with large data volumes.

---

# 68. Bulk Actions

If the user needs to perform an operation on multiple Leads, can provide:

```text
Select
Select All
Bulk Actions
```

Like:

```text
Export
Change Status
Delete
```

But do not add unneeded Bulk Actions.

---

# 69. Confirmation for Bulk Operations

Every Bulk Action that may lead to data loss must be clear and subject to confirmation.

Example:

```text
Delete 25 selected leads?

[Cancel] [Delete]
```

---

# 70. Visual Performance Rule

Do not use heavy Components without need.

The interface must be:

```text
Fast
Responsive
Lightweight
```

Especially in:

* Tables.
* Search.
* Filtering.
* Large data pages.

---

# 71. UI and Logic Separation Rule

The interface must not contain:

* SQL.
* Complex Business Logic.
* Duplicate Detection Logic.
* Data Collection Logic.
* Parsing Logic.

Correct path:

```text
UI
  ↓
Service
  ↓
Business Logic
  ↓
Repository / Collector
```

---

# 72. UI State Rule

Interface states must be clear.

Example:

```text
Idle
Loading
Success
Error
Empty
Disabled
```

Do not leave the user in front of an interface where they don't know if the operation is working or not.

---

# 73. Don't Hide Important Operations Rule

Basic actions must be easily accessible.

Do not put:

```text
Start Collection
Save
Export
```

Inside multiple nested menus if these operations are used constantly.

---

# 74. No Page Clutter Rule

If a page comes to contain many elements:

```text
Search
Filters
Buttons
Cards
Table
Statistics
Actions
Panels
```

Must re-evaluate the design.

Do not try to solve everything by adding more sections.

Better to simplify the page.

---

# 75. Checklist Before Creating or Modifying a Page

Codex must verify:

* [ ] What is the page's core task?
* [ ] Is Navigation clear?
* [ ] Is the page title clear?
* [ ] Is there a clear Primary Action?
* [ ] Is Search necessary?
* [ ] Are Filters necessary?
* [ ] Are all displayed columns necessary?
* [ ] Does an Empty State exist?
* [ ] Does a Loading State exist when needed?
* [ ] Is the Error State clear?
* [ ] Is the design consistent with the rest of the application?
* [ ] Is there a Component that can be reused?
* [ ] Were unnecessary visual elements added?
* [ ] Was a Dashboard or Chart added without a requirement?
* [ ] Is there visual clutter?
* [ ] Does the interface separate UI from Business Logic?

---

# 76. Checklist Before Adding a New Visual Element

Before adding:

```text
Card
Chart
Widget
Statistic
Animation
Badge
Panel
```

Codex must ask:

1. What is its functional purpose?
2. Does it help the user?
3. Can the same information be displayed in a simpler way?
4. Is there a similar Component?
5. Will it increase page clutter?
6. Is it required by Business Requirements?

If no clear benefit exists, do not add it.

---

# 77. Final Principle

The program interface is not a design exhibition.

Its primary goal is to enable the user to:

```text
Collect Leads
↓
Review Data
↓
Manage Companies
↓
Manage Contacts
↓
Manage Domains
↓
Manage Emails
↓
Manage Lead Status
↓
Export / Use Data
```

Therefore the design must be:

```text
Simple
Clear
Professional
Consistent
Task-oriented
Data-focused
```

And must avoid:

```text
Unnecessary Dashboards
Unnecessary Charts
Unnecessary Analytics
Unnecessary Cards
Unnecessary Animations
Unnecessary Complexity
```

Most important rule:

> Do not add an element to the interface because it makes it look more professional; add it only if it makes the program more useful, clearer, or easier to use.

Second rule:

> Simplicity is not a lack of design, but an intentional design decision.

Third rule:

> When choosing between an interface with many elements and a simpler one that accomplishes the same task clearly, choose the simpler interface.
