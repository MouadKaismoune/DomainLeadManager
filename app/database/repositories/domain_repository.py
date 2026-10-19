"""Domain persistence operations."""

from app.database.connection import get_connection


class DomainRepository:
    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT id, domain_name, status, notes FROM domains ORDER BY domain_name"
            ).fetchall()
        return [dict(row) for row in rows]

    def create(self, domain_name: str, normalized_domain: str, extension: str) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO domains (domain_name, normalized_domain, extension)
                VALUES (?, ?, ?)
                """,
                (domain_name, normalized_domain, extension),
            )
        return int(cursor.lastrowid)

    def update(self, domain_id: int, domain_name: str, normalized_domain: str, extension: str) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE domains
                SET domain_name = ?, normalized_domain = ?, extension = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (domain_name, normalized_domain, extension, domain_id),
            )

    def delete(self, domain_id: int) -> None:
        with get_connection() as connection:
            connection.execute("DELETE FROM domains WHERE id = ?", (domain_id,))
