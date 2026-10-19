"""Display-level aggregation for the workspace tables."""

EMPTY_VALUE = "—"


def _append_unique(values: list[str], value: object) -> None:
    text = str(value).strip() if value is not None else ""
    if text and text not in values:
        values.append(text)


def aggregate_overview_rows(rows: list[dict]) -> list[dict]:
    """Collapse the raw lead/contact/email join into one row per contact.

    The repository returns a row for every company-email x contact-email
    combination. That is useful for searching but unreadable in a table, so
    emails are collected per lead/contact and joined for display.
    """
    grouped: dict[tuple, dict] = {}
    for row in rows:
        key = (row.get("lead_id"), row.get("contact_id"))
        group = grouped.get(key)
        if group is None:
            group = {
                "lead_id": row.get("lead_id"),
                "contact_id": row.get("contact_id"),
                "company_name": row.get("company_name") or "",
                "website": row.get("website") or "",
                "address": row.get("address") or "",
                "contact_name": row.get("contact_name") or "",
                "priority": row.get("priority") or "",
                "notes": row.get("notes") or "",
                "_company_emails": [],
                "_contact_emails": [],
            }
            grouped[key] = group
        _append_unique(group["_company_emails"], row.get("company_email"))
        _append_unique(group["_contact_emails"], row.get("contact_email"))

    result = []
    for group in grouped.values():
        group["company_email"] = ", ".join(group.pop("_company_emails"))
        group["contact_email"] = ", ".join(group.pop("_contact_emails"))
        result.append(group)
    return result


def aggregate_contact_rows(rows: list[dict]) -> list[dict]:
    """Collapse the contact/email join into one row per contact."""
    grouped: dict[object, dict] = {}
    for row in rows:
        key = row.get("id")
        if key is None:
            key = (row.get("full_name"), row.get("company_name"))
        group = grouped.get(key)
        if group is None:
            group = {**row, "emails": []}
            grouped[key] = group
        _append_unique(group["emails"], row.get("email"))

    result = []
    for group in grouped.values():
        group["email"] = ", ".join(group.pop("emails"))
        result.append(group)
    return result


def display_value(value: object) -> str:
    """Empty database values are shown as a muted dash, never as 'None'."""
    if value is None:
        return EMPTY_VALUE
    text = str(value).strip()
    return text or EMPTY_VALUE
