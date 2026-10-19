"""Domain business operations."""

import sqlite3

from app.core.exceptions import DuplicateRecordError, ValidationError
from app.core.utilities import extract_extension, is_valid_domain, normalize_domain
from app.database.repositories.domain_repository import DomainRepository


class DomainService:
    def __init__(self, repository: DomainRepository | None = None) -> None:
        self.repository = repository or DomainRepository()

    def list_domains(self) -> list[dict]:
        return self.repository.list_all()

    def create_domain(self, domain_name: str) -> int:
        cleaned_name, normalized, extension = self._validate(domain_name)
        try:
            return self.repository.create(cleaned_name, normalized, extension)
        except sqlite3.IntegrityError as error:
            raise DuplicateRecordError("This domain already exists.") from error

    def update_domain(self, domain_id: int, domain_name: str) -> None:
        cleaned_name, normalized, extension = self._validate(domain_name)
        try:
            self.repository.update(domain_id, cleaned_name, normalized, extension)
        except sqlite3.IntegrityError as error:
            raise DuplicateRecordError("This domain already exists.") from error

    def delete_domain(self, domain_id: int) -> None:
        self.repository.delete(domain_id)

    @staticmethod
    def _validate(domain_name: str) -> tuple[str, str, str]:
        cleaned_name = domain_name.strip()
        normalized = normalize_domain(cleaned_name)
        if not is_valid_domain(cleaned_name):
            raise ValidationError("Enter a valid domain, for example example.com.")
        return cleaned_name, normalized, extract_extension(normalized)
