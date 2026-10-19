"""Company business operations."""

import sqlite3

from app.core.exceptions import DuplicateRecordError, ValidationError
from app.core.utilities import normalize_text
from app.database.repositories.company_repository import CompanyRepository


class CompanyService:
    def __init__(self, repository: CompanyRepository | None = None) -> None:
        self.repository = repository or CompanyRepository()

    def list_companies(self) -> list[dict]:
        return self.repository.list_all()

    def create_company(self, company_name: str, website: str = "") -> int:
        cleaned_name = company_name.strip()
        if not cleaned_name:
            raise ValidationError("Company name is required.")
        try:
            return self.repository.create(cleaned_name, normalize_text(cleaned_name), website.strip())
        except sqlite3.IntegrityError as error:
            raise DuplicateRecordError("This company could not be saved as entered.") from error
