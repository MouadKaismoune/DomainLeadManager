---
name: getting-started
description: Provides a reading priority order and quick-start guide for CODEX to use the project's skills effectively without being overwhelmed.
---

# Getting Started

## Purpose

This skill is the **entry point** for any AI agent (Codex, OpenCode, or similar) working on this project.

The project contains 12 skills. Reading all of them at once would be inefficient for a simple start.

This skill provides:

1. A **reading priority order** so the agent knows which skills to read first.
2. A **quick context summary** of the project.
3. A **decision rule** for when to read each additional skill.
4. A **conflict resolution rule** when two skills disagree.

---

## 1. Project Quick Summary

```text
Project Type:     Desktop application
Purpose:          Domain-investing lead management
Database:         SQLite (local)
UI Framework:     Not yet decided (likely PyQt, Tkinter, or similar)
Business Domain:  Domain Lead Generation
Core Workflow:    Domain → Company → Contact → Lead
Architecture:     UI → Service → Repository → Database
```

---

## 2. Skills Available (12 Total)

| File | Purpose |
|------|---------|
| `project-overview.md` | What the project is, scope, goals |
| `architecture.md` | Layered architecture, separation of concerns |
| `business-domain.md` | Core entities (Domain, Company, Contact, Lead) |
| `business-rules.md` | Operational rules for the business domain |
| `database-rules.md` | SQLite-specific rules, normalization, constraints |
| `project-structure.md` | Folder/file organization |
| `coding-rules.md` | Python coding standards |
| `ui-guidelines.md` | Interface design rules |
| `testing.md` | Testing strategies and rules |
| `error-handling.md` | Error handling philosophy |
| `ai-development-rules.md` | How the AI agent should work |

---

## 3. Reading Priority for a Simple Project Start

For a **simple project start**, follow this order:

### 🔴 Priority 1 — Must Read First (Before Writing Any Code)

| Order | File | Why |
|-------|------|-----|
| 1 | `project-overview.md` | Understand what we are building |
| 2 | `architecture.md` | Understand the layer structure |
| 3 | `business-domain.md` | Understand the core entities |
| 4 | `database-rules.md` | Understand how to store data correctly |
| 5 | `project-structure.md` | Know where to put files |

After reading these 5 skills, you have enough context to start a simple V1.

---

### 🟡 Priority 2 — Read When Implementing the Feature

| When | File |
|------|------|
| Writing any code | `coding-rules.md` |
| Creating a new Service, Repository, or UI page | `business-rules.md` |
| Handling errors, validation, exceptions | `error-handling.md` |
| Building any user interface | `ui-guidelines.md` |
| Writing tests | `testing.md` |
| Stuck or unsure how to behave | `ai-development-rules.md` |

---

### 🟢 Priority 3 — Reference Only (Do Not Read Unless Needed)

These skills are **exhaustive reference material**. Don't read them cover-to-cover.

* Read specific sections only when the task requires it.
* Use the table of contents to jump to the relevant rule.

All 12 skills fall into this category once you have read Priority 1.

---

## 4. When the User Asks for a Feature

Use this workflow:

```text
1. Understand the request
        ↓
2. Read relevant Skills (Priority 1 + relevant Priority 2)
        ↓
3. Inspect existing project code (if any)
        ↓
4. Identify correct layer (UI / Service / Repository)
        ↓
5. Plan the minimal change
        ↓
6. Implement
        ↓
7. Test (at least the critical path)
        ↓
8. Verify behavior
```

---

## 5. Decision Tree: Which Skill to Read?

```text
Is the request about...?
│
├── "What is this project?"           → project-overview.md
├── "How is the code organized?"      → architecture.md + project-structure.md
├── "What is a Domain/Company/Lead?"  → business-domain.md
├── "How should I save/manage data?"  → business-rules.md + database-rules.md
├── "How do I write Python code?"     → coding-rules.md
├── "How should the UI look?"         → ui-guidelines.md
├── "How should I handle errors?"     → error-handling.md
├── "How should I test this?"         → testing.md
└── "How should I behave as an AI?"   → ai-development-rules.md
```

---

## 6. Conflict Resolution Rule

If two skills give contradictory instructions, follow this priority:

```text
1. project-overview.md        (project definition, scope, canonical lists)
2. business-domain.md         (entity definitions and relationships)
3. business-rules.md          (operational rules)
4. architecture.md            (architectural rules)
5. database-rules.md          (database rules)
6. ui-guidelines.md           (UI rules)
7. coding-rules.md            (coding standards)
8. testing.md                 (testing rules)
9. error-handling.md          (error handling)
10. ai-development-rules.md   (AI agent behavior)
```

**Most important:** If you find a conflict that is not resolvable by this priority order, ask the user.

---

## 7. The Canonical Lists

Some lists are defined in `project-overview.md` and must be used everywhere else without modification:

### Lead Status (canonical 7 values)

```text
new
researching
ready
contacted
interested
not_interested
archived
```

**Do NOT use** generic CRM statuses like `Qualified`, `Negotiating`, `Won`, `Lost` unless the user explicitly requests them.

### Lead Priority (canonical 3 values)

```text
low
normal
high
```

### Architecture Flow (canonical)

```text
UI
  ↓
Service
  ↓
Repository
  ↓
SQLite Database
```

---

## 8. Quick Examples

### Example 1: User asks "Add a new Company"

**Skills to read:** project-overview.md (skim), business-domain.md (Company section), business-rules.md (Company section), project-structure.md (services + repositories), coding-rules.md (Python style).

**Layer to modify:** `CompanyService` (business logic) + `CompanyRepository` (persistence) + UI form.

**Don't do:** Put SQL inside the UI, or put duplicate-detection logic in the Repository.

### Example 2: User asks "Why is the database locked?"

**Skills to read:** database-rules.md, error-handling.md.

**Don't do:** Add a `try/except: pass` to hide the error. Read the error, understand the root cause, then fix properly.

### Example 3: User asks "Add a Dashboard with statistics"

**Skills to read:** ui-guidelines.md (No Dashboard rule), project-overview.md (V1 scope).

**Don't do:** Add the Dashboard. The project explicitly avoids dashboards in V1. Tell the user this and ask if they really need it.

---

## 9. What NOT to Do

* ❌ Do NOT read all 12 skills before writing any code.
* ❌ Do NOT invent new status values (use the canonical Lead Status list).
* ❌ Do NOT put SQL inside UI code.
* ❌ Do NOT auto-merge or auto-delete "possible duplicates".
* ❌ Do NOT add a Dashboard, Charts, or Analytics unless explicitly requested.
* ❌ Do NOT hide exceptions with `try/except: pass`.
* ❌ Do NOT delete data as a workaround for any problem.
* ❌ Do NOT rewrite working code without a real reason.

---

## 10. Red Flags — Stop and Ask the User

If the user asks you to do any of the following, **stop and confirm** before implementing:

* Delete multiple records at once.
* Add a feature explicitly listed in "NOT Required in V1" (project-overview.md section 18).
* Change the canonical Lead Status list.
* Change the database schema in a destructive way.
* Remove or weaken existing tests.
* Disable safety checks like foreign keys or unique constraints.
* Auto-merge or auto-delete "possible duplicates".

---

## 11. Final Rule

The project should evolve **incrementally and safely**.

```text
Understand  → Inspect  → Plan  → Change  → Test  → Verify
```

Not:

```text
Request  → Guess  → Edit files
```

Start small. Make minimal changes. Preserve existing behavior. Ask when in doubt.
