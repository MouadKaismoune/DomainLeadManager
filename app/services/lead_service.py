"""Lead business operations."""

import sqlite3

from app.core.exceptions import DuplicateRecordError
from app.database.repositories.lead_repository import LeadRepository


class LeadService:
    def __init__(self, repository: LeadRepository | None = None) -> None:
        self.repository = repository or LeadRepository()

    def list_leads(self) -> list[dict]:
        return self.repository.list_all()

    def list_leads_for_domain(self, domain_id: int) -> list[dict]:
        return self.repository.list_by_domain(domain_id)

    def create_lead(self, domain_id: int, company_id: int) -> int:
        try:
            return self.repository.create(domain_id, company_id)
        except sqlite3.IntegrityError as error:
            raise DuplicateRecordError("This domain-company lead already exists.") from error
