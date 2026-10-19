"""Lead persistence operations."""

from app.database.connection import get_connection


class LeadRepository:
    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT domain_leads.id, domains.domain_name, companies.company_name,
                       domain_leads.status, domain_leads.priority
                FROM domain_leads
                JOIN domains ON domains.id = domain_leads.domain_id
                JOIN companies ON companies.id = domain_leads.company_id
                ORDER BY domain_leads.created_at DESC
                """
            ).fetchall()
        return [dict(row) for row in rows]

    def list_by_domain(self, domain_id: int) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT domain_leads.id, domains.domain_name, companies.company_name,
                       domain_leads.status, domain_leads.priority
                FROM domain_leads
                JOIN domains ON domains.id = domain_leads.domain_id
                JOIN companies ON companies.id = domain_leads.company_id
                WHERE domain_leads.domain_id = ?
                ORDER BY domain_leads.created_at DESC
                """,
                (domain_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def create(self, domain_id: int, company_id: int) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO domain_leads (domain_id, company_id) VALUES (?, ?)",
                (domain_id, company_id),
            )
        return int(cursor.lastrowid)
