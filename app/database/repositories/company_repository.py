"""Company persistence operations."""

from app.database.connection import get_connection


class CompanyRepository:
    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT id, company_name, website, city, country FROM companies ORDER BY company_name"
            ).fetchall()
        return [dict(row) for row in rows]

    def create(self, company_name: str, normalized_name: str, website: str = "") -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO companies (company_name, normalized_name, website, normalized_website)
                VALUES (?, ?, ?, ?)
                """,
                (company_name, normalized_name, website or None, website or None),
            )
        return int(cursor.lastrowid)
