"""Persistence for data scoped to one domain lead."""

import sqlite3

from app.database.connection import get_connection


class WorkspaceRepository:
    def list_domain_workspace(self, domain_id: int) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT dl.id AS lead_id,
                       COALESCE(dl.company_name, companies.company_name) AS company_name,
                       CASE WHEN dl.company_name IS NULL THEN companies.website ELSE dl.company_website END AS website,
                       CASE WHEN dl.company_name IS NULL THEN companies.address ELSE dl.company_address END AS address,
                       dl.priority, dl.notes,
                       dlc.id AS contact_id, dlc.full_name AS contact_name,
                       dlce.id AS contact_email_id, dlce.email AS contact_email,
                       dlce_company.id AS company_email_id,
                       dlce_company.email AS company_email
                FROM domain_leads AS dl
                JOIN companies ON companies.id = dl.company_id
                LEFT JOIN domain_lead_company_emails AS dlce_company
                    ON dlce_company.domain_lead_id = dl.id
                LEFT JOIN domain_lead_contacts AS dlc
                    ON dlc.domain_lead_id = dl.id
                LEFT JOIN domain_lead_contact_emails AS dlce
                    ON dlce.domain_lead_contact_id = dlc.id
                WHERE dl.domain_id = ?
                ORDER BY companies.company_name, dlc.full_name, dlce.email
                """,
                (domain_id,),
            ).fetchall()
        return [dict(row) for row in rows]

    def list_domain_contacts(self, domain_id: int) -> list[dict]:
        with get_connection() as connection:
            contacts = connection.execute(
                """
                SELECT dlc.id, dlc.full_name, dlc.job_title, dlc.department,
                       COALESCE(dl.company_name, companies.company_name) AS company_name
                FROM domain_lead_contacts AS dlc
                JOIN domain_leads AS dl ON dl.id = dlc.domain_lead_id
                JOIN companies ON companies.id = dl.company_id
                WHERE dl.domain_id = ?
                ORDER BY dlc.full_name
                """,
                (domain_id,),
            ).fetchall()
            result = []
            for row in contacts:
                contact = dict(row)
                emails = [item["email"] for item in connection.execute(
                    "SELECT email FROM domain_lead_contact_emails WHERE domain_lead_contact_id = ? ORDER BY id",
                    (contact["id"],),
                )]
                phones = ", ".join(item["phone"] for item in connection.execute(
                    "SELECT phone FROM domain_lead_contact_phones WHERE domain_lead_contact_id = ? ORDER BY id",
                    (contact["id"],),
                ))
                socials = ", ".join(
                    f"{item['platform']}: {item['url']}" for item in connection.execute(
                        "SELECT platform, url FROM domain_lead_contact_socials WHERE domain_lead_contact_id = ? ORDER BY id",
                        (contact["id"],),
                    )
                )
                for email in emails or [""]:
                    result.append({**contact, "email": email, "phones": phones, "socials": socials})
        return result

    def get_edit_record(self, lead_id: int) -> dict:
        with get_connection() as connection:
            lead = connection.execute(
                """
                SELECT dl.id AS lead_id, dl.company_id, dl.priority, dl.notes,
                       COALESCE(dl.company_name, companies.company_name) AS company_name,
                       CASE WHEN dl.company_name IS NULL THEN companies.website ELSE dl.company_website END AS website,
                       CASE WHEN dl.company_name IS NULL THEN companies.description ELSE dl.company_description END AS description,
                       CASE WHEN dl.company_name IS NULL THEN companies.address ELSE dl.company_address END AS address,
                       CASE WHEN dl.company_name IS NULL THEN companies.city ELSE dl.company_city END AS city,
                       CASE WHEN dl.company_name IS NULL THEN companies.state ELSE dl.company_state END AS state,
                       CASE WHEN dl.company_name IS NULL THEN companies.country ELSE dl.company_country END AS country
                FROM domain_leads AS dl
                JOIN companies ON companies.id = dl.company_id
                WHERE dl.id = ?
                """,
                (lead_id,),
            ).fetchone()
            if not lead:
                raise sqlite3.IntegrityError("lead does not exist")
            result = dict(lead)
            company_id = int(lead["company_id"])
            legacy = lead["company_name"] is None
            result["company_emails"] = self._values_or_fallback(
                connection, "domain_lead_company_emails", "domain_lead_id", lead_id,
                "email", "company_emails", company_id, legacy
            )
            result["company_phones"] = self._values_or_fallback(
                connection, "domain_lead_company_phones", "domain_lead_id", lead_id,
                "phone", "company_phones", company_id, legacy
            )
            result["company_socials"] = self._socials_or_fallback(connection, lead_id, company_id, True, legacy)
            result["contacts"] = self._lead_contacts(connection, lead_id, company_id, legacy)
        return result

    @staticmethod
    def _values_or_fallback(connection, table, foreign_key, foreign_id, value_column, fallback_table, company_id, allow_fallback):
        values = [row[value_column] for row in connection.execute(
            f"SELECT {value_column} FROM {table} WHERE {foreign_key} = ? ORDER BY id", (foreign_id,)
        )]
        if values or not allow_fallback:
            return values
        return [row[value_column] for row in connection.execute(
            f"SELECT {value_column} FROM {fallback_table} WHERE company_id = ? ORDER BY id", (company_id,)
        )]

    @staticmethod
    def _socials_or_fallback(connection, lead_id, company_id, company_level, allow_fallback):
        table = "domain_lead_company_socials" if company_level else "domain_lead_contact_socials"
        foreign_key = "domain_lead_id" if company_level else "domain_lead_contact_id"
        fallback = "company_socials" if company_level else "contact_socials"
        values = [dict(row) for row in connection.execute(
            f"SELECT platform, url FROM {table} WHERE {foreign_key} = ? ORDER BY id", (lead_id,)
        )]
        if values or company_level is False or not allow_fallback:
            return values
        return [dict(row) for row in connection.execute(
            f"SELECT platform, url FROM {fallback} WHERE company_id = ? ORDER BY id", (company_id,)
        )]

    @classmethod
    def _lead_contacts(cls, connection, lead_id, company_id, allow_fallback):
        contacts = [dict(row) for row in connection.execute(
            "SELECT id, full_name, job_title, department FROM domain_lead_contacts WHERE domain_lead_id = ? ORDER BY id",
            (lead_id,),
        )]
        if not contacts and allow_fallback:
            contacts = [dict(row) for row in connection.execute(
                "SELECT id, full_name, job_title, department FROM contacts WHERE company_id = ? ORDER BY id",
                (company_id,),
            )]
            for contact in contacts:
                contact_id = contact["id"]
                contact["emails"] = [row["email"] for row in connection.execute(
                    "SELECT email FROM contact_emails WHERE contact_id = ? ORDER BY id", (contact_id,)
                )]
                contact["phones"] = [row["phone"] for row in connection.execute(
                    "SELECT phone FROM contact_phones WHERE contact_id = ? ORDER BY id", (contact_id,)
                )]
                contact["socials"] = [dict(row) for row in connection.execute(
                    "SELECT platform, url FROM contact_socials WHERE contact_id = ? ORDER BY id", (contact_id,)
                )]
            return contacts
        if not contacts:
            return []
        for contact in contacts:
            contact_id = contact["id"]
            contact["emails"] = [row["email"] for row in connection.execute(
                "SELECT email FROM domain_lead_contact_emails WHERE domain_lead_contact_id = ? ORDER BY id", (contact_id,)
            )]
            contact["phones"] = [row["phone"] for row in connection.execute(
                "SELECT phone FROM domain_lead_contact_phones WHERE domain_lead_contact_id = ? ORDER BY id", (contact_id,)
            )]
            contact["socials"] = [dict(row) for row in connection.execute(
                "SELECT platform, url FROM domain_lead_contact_socials WHERE domain_lead_contact_id = ? ORDER BY id", (contact_id,)
            )]
        return contacts

    def add_domain_prospect(self, domain_id, company, contacts, company_emails, company_phones, company_socials, priority, notes):
        with get_connection() as connection:
            company_row = connection.execute(
                "SELECT id FROM companies WHERE normalized_name = ?", (company["normalized_name"],)
            ).fetchone()
            if company_row:
                company_id = int(company_row["id"])
            else:
                cursor = connection.execute(
                    "INSERT INTO companies (company_name, normalized_name) VALUES (?, ?)",
                    (company["name"], company["normalized_name"]),
                )
                company_id = int(cursor.lastrowid)
            lead_cursor = connection.execute(
                """
                INSERT INTO domain_leads
                    (domain_id, company_id, company_name, company_website, company_description,
                     company_address, company_city, company_state, company_country,
                     priority, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (domain_id, company_id, company["name"], company["website"] or None, company["description"] or None,
                 company["address"] or None, company["city"] or None, company["state"] or None,
                 company["country"] or None, priority, notes or None),
            )
            lead_id = int(lead_cursor.lastrowid)
            self._insert_lead_values(connection, lead_id, company_emails, company_phones, company_socials, contacts)
            return lead_id

    def update_workspace_record(self, record: dict) -> None:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE domain_leads
                SET company_name = ?, company_website = ?, company_description = ?, company_address = ?,
                    company_city = ?, company_state = ?, company_country = ?,
                    priority = ?, notes = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (record["company_name"] or None, record["website"] or None, record["description"] or None, record["address"] or None,
                 record["city"] or None, record["state"] or None, record["country"] or None,
                 record["priority"], record["notes"] or None, record["lead_id"]),
            )
            connection.execute("DELETE FROM domain_lead_company_emails WHERE domain_lead_id = ?", (record["lead_id"],))
            connection.execute("DELETE FROM domain_lead_company_phones WHERE domain_lead_id = ?", (record["lead_id"],))
            connection.execute("DELETE FROM domain_lead_company_socials WHERE domain_lead_id = ?", (record["lead_id"],))
            connection.execute("DELETE FROM domain_lead_contacts WHERE domain_lead_id = ?", (record["lead_id"],))
            self._insert_lead_values(connection, record["lead_id"], record["company_emails"], record["company_phones"], record["company_socials"], record["contacts"])

    @staticmethod
    def _insert_lead_values(connection, lead_id, company_emails, company_phones, company_socials, contacts):
        for email in company_emails:
            connection.execute("INSERT INTO domain_lead_company_emails (domain_lead_id, email, normalized_email) VALUES (?, ?, ?)", (lead_id, email, email))
        for phone in company_phones:
            connection.execute("INSERT INTO domain_lead_company_phones (domain_lead_id, phone, normalized_phone) VALUES (?, ?, ?)", (lead_id, phone, phone))
        for social in company_socials:
            connection.execute("INSERT INTO domain_lead_company_socials (domain_lead_id, platform, url, normalized_url) VALUES (?, ?, ?, ?)", (lead_id, social["platform"], social["url"], social["url"]))
        for contact in contacts:
            cursor = connection.execute(
                "INSERT INTO domain_lead_contacts (domain_lead_id, full_name, normalized_name, job_title, department) VALUES (?, ?, ?, ?, ?)",
                (lead_id, contact["name"], contact["normalized_name"], contact["job_title"] or None, contact["department"] or None),
            )
            contact_id = int(cursor.lastrowid)
            for email in contact["emails"]:
                connection.execute("INSERT INTO domain_lead_contact_emails (domain_lead_contact_id, email, normalized_email) VALUES (?, ?, ?)", (contact_id, email, email))
            for phone in contact["phones"]:
                connection.execute("INSERT INTO domain_lead_contact_phones (domain_lead_contact_id, phone, normalized_phone) VALUES (?, ?, ?)", (contact_id, phone, phone))
            for social in contact["socials"]:
                connection.execute("INSERT INTO domain_lead_contact_socials (domain_lead_contact_id, platform, url, normalized_url) VALUES (?, ?, ?, ?)", (contact_id, social["platform"], social["url"], social["url"]))
