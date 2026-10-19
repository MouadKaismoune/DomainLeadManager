"""Business operations for the selected domain workspace."""

import re
import sqlite3

from app.core.exceptions import DuplicateRecordError, ValidationError
from app.core.utilities import normalize_text
from app.database.repositories.workspace_repository import WorkspaceRepository


class WorkspaceService:
    def __init__(self, repository: WorkspaceRepository | None = None) -> None:
        self.repository = repository or WorkspaceRepository()

    def list_domain_workspace(self, domain_id: int) -> list[dict]:
        return self.repository.list_domain_workspace(domain_id)

    def list_domain_contacts(self, domain_id: int) -> list[dict]:
        return self.repository.list_domain_contacts(domain_id)

    def get_edit_record(self, lead_id: int) -> dict:
        return self.repository.get_edit_record(lead_id)

    def add_prospect(self, domain_id: int, data: dict) -> int:
        company = data["company"]
        company_name = company["name"].strip()
        if not company_name:
            raise ValidationError("Company or contact name is required.")
        if data["priority"] not in ("low", "normal", "high"):
            raise ValidationError("Choose a valid priority.")

        contacts = []
        for raw_contact in data["contacts"]:
            name = raw_contact["name"].strip()
            emails = self._valid_emails(raw_contact["emails"])
            if name or emails:
                if not name:
                    raise ValidationError("Every email group needs a responsible person name.")
                contacts.append(
                    {
                        **raw_contact,
                        "name": name,
                        "normalized_name": normalize_text(name),
                        "emails": emails,
                        "phones": self._clean_values(raw_contact["phones"]),
                        "socials": self._clean_socials(raw_contact["socials"]),
                    }
                )

        try:
            return self.repository.add_domain_prospect(
                domain_id=domain_id,
                company={
                    **company,
                    "name": company_name,
                    "normalized_name": normalize_text(company_name),
                },
                contacts=contacts,
                company_emails=self._valid_emails(data["company_emails"]),
                company_phones=self._clean_values(data["company_phones"]),
                company_socials=self._clean_socials(data["company_socials"]),
                priority=data["priority"],
                notes=data["notes"].strip(),
            )
        except sqlite3.IntegrityError as error:
            message = str(error).lower()
            if "domain_leads" in message:
                raise DuplicateRecordError("This company is already linked to this domain.") from error
            if "email" in message:
                raise DuplicateRecordError("This email is already assigned elsewhere.") from error
            raise DuplicateRecordError("Some of this information already exists.") from error

    def update_record(self, data: dict) -> None:
        company = data["company"]
        company_name = company["name"].strip()
        if not company_name:
            raise ValidationError("Company name is required.")
        if data["priority"] not in ("low", "normal", "high"):
            raise ValidationError("Choose a valid priority.")
        contacts = []
        for raw_contact in data["contacts"]:
            name = raw_contact["name"].strip()
            emails = self._valid_emails(raw_contact["emails"])
            if name or emails:
                if not name:
                    raise ValidationError("Every email group needs a responsible person name.")
                contacts.append(
                    {
                        **raw_contact,
                        "name": name,
                        "normalized_name": normalize_text(name),
                        "emails": emails,
                        "phones": self._clean_values(raw_contact["phones"]),
                        "socials": self._clean_socials(raw_contact["socials"]),
                    }
                )
        try:
            self.repository.update_workspace_record(
                {
                    "lead_id": data["lead_id"],
                    "company": {**company, "name": company_name, "normalized_name": normalize_text(company_name)},
                    "company_name": company_name,
                    "normalized_company_name": normalize_text(company_name),
                    "website": company["website"].strip(),
                    "description": company["description"].strip(),
                    "address": company["address"].strip(),
                    "city": company["city"].strip(),
                    "state": company["state"].strip(),
                    "country": company["country"].strip(),
                    "company_emails": self._valid_emails(data["company_emails"]),
                    "company_phones": self._clean_values(data["company_phones"]),
                    "company_socials": self._clean_socials(data["company_socials"]),
                    "contacts": contacts,
                    "priority": data["priority"],
                    "notes": data["notes"].strip(),
                }
            )
        except sqlite3.IntegrityError as error:
            if "email" in str(error).lower():
                raise DuplicateRecordError("This email is already assigned to another contact.") from error
            raise DuplicateRecordError("The record could not be updated as entered.") from error

    @staticmethod
    def _clean_values(values: list[str]) -> list[str]:
        return list(dict.fromkeys(value.strip() for value in values if value.strip()))

    @classmethod
    def _valid_emails(cls, values: list[str]) -> list[str]:
        emails = [value.strip().lower() for value in values if value.strip()]
        for email in emails:
            if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
                raise ValidationError(f"Invalid email address: {email}")
        return list(dict.fromkeys(emails))

    @classmethod
    def _clean_socials(cls, values: list[dict]) -> list[dict]:
        cleaned = []
        for social in values:
            platform = social["platform"].strip()
            url = social["url"].strip()
            if platform or url:
                if not platform or not url:
                    raise ValidationError("Every social account needs a platform and URL.")
                cleaned.append({"platform": platform, "url": url})
        return cleaned
