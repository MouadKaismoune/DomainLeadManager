"""SQLite connection and schema initialization."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.config.settings import DATA_DIR, DATABASE_PATH, SCHEMA_PATH


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Open a transaction-scoped SQLite connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database() -> Path:
    """Create the application database from the checked-in schema."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with get_connection() as connection:
        existing = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'domains'"
        ).fetchone()
        if existing:
            _ensure_workspace_schema(connection)
            return DATABASE_PATH
        connection.executescript(schema)
        _ensure_workspace_schema(connection)
    return DATABASE_PATH


def _ensure_workspace_schema(connection: sqlite3.Connection) -> None:
    """Apply the domain-scoped workspace schema to existing databases."""
    columns = {
        row["name"] for row in connection.execute("PRAGMA table_info(domain_leads)")
    }
    for column in (
        "company_name",
        "company_website",
        "company_description",
        "company_address",
        "company_city",
        "company_state",
        "company_country",
    ):
        if column not in columns:
            connection.execute(f"ALTER TABLE domain_leads ADD COLUMN {column} TEXT")

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS domain_lead_company_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_lead_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            normalized_email TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE,
            UNIQUE (domain_lead_id, normalized_email)
        );
        CREATE TABLE IF NOT EXISTS domain_lead_company_phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_lead_id INTEGER NOT NULL,
            phone TEXT NOT NULL,
            normalized_phone TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE,
            UNIQUE (domain_lead_id, normalized_phone)
        );
        CREATE TABLE IF NOT EXISTS domain_lead_company_socials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_lead_id INTEGER NOT NULL,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            normalized_url TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS domain_lead_contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_lead_id INTEGER NOT NULL,
            full_name TEXT NOT NULL,
            normalized_name TEXT NOT NULL,
            job_title TEXT,
            department TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (domain_lead_id) REFERENCES domain_leads(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS domain_lead_contact_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_lead_contact_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            normalized_email TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (domain_lead_contact_id) REFERENCES domain_lead_contacts(id) ON DELETE CASCADE,
            UNIQUE (domain_lead_contact_id, normalized_email)
        );
        CREATE TABLE IF NOT EXISTS domain_lead_contact_phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_lead_contact_id INTEGER NOT NULL,
            phone TEXT NOT NULL,
            normalized_phone TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (domain_lead_contact_id) REFERENCES domain_lead_contacts(id) ON DELETE CASCADE,
            UNIQUE (domain_lead_contact_id, normalized_phone)
        );
        CREATE TABLE IF NOT EXISTS domain_lead_contact_socials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain_lead_contact_id INTEGER NOT NULL,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            normalized_url TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (domain_lead_contact_id) REFERENCES domain_lead_contacts(id) ON DELETE CASCADE
        );
        """
    )
    _migrate_legacy_workspace_records(connection)


def _migrate_legacy_workspace_records(connection: sqlite3.Connection) -> None:
    """Snapshot old shared company/contact data into each existing lead."""
    legacy_leads = connection.execute(
        """
        SELECT dl.id, dl.company_id, c.company_name, c.website, c.description,
               c.address, c.city, c.state, c.country
        FROM domain_leads AS dl
        JOIN companies AS c ON c.id = dl.company_id
        WHERE dl.company_name IS NULL
        """
    ).fetchall()
    for lead in legacy_leads:
        lead_id = int(lead["id"])
        company_id = int(lead["company_id"])
        connection.execute(
            """
            UPDATE domain_leads
            SET company_name = ?, company_website = ?, company_description = ?,
                company_address = ?, company_city = ?, company_state = ?, company_country = ?
            WHERE id = ?
            """,
            (lead["company_name"], lead["website"], lead["description"], lead["address"],
             lead["city"], lead["state"], lead["country"], lead_id),
        )
        for row in connection.execute("SELECT email FROM company_emails WHERE company_id = ?", (company_id,)):
            connection.execute(
                "INSERT OR IGNORE INTO domain_lead_company_emails (domain_lead_id, email, normalized_email) VALUES (?, ?, ?)",
                (lead_id, row["email"], row["email"].lower()),
            )
        for row in connection.execute("SELECT phone FROM company_phones WHERE company_id = ?", (company_id,)):
            connection.execute(
                "INSERT OR IGNORE INTO domain_lead_company_phones (domain_lead_id, phone, normalized_phone) VALUES (?, ?, ?)",
                (lead_id, row["phone"], row["phone"]),
            )
        for row in connection.execute("SELECT platform, url FROM company_socials WHERE company_id = ?", (company_id,)):
            connection.execute(
                "INSERT INTO domain_lead_company_socials (domain_lead_id, platform, url, normalized_url) VALUES (?, ?, ?, ?)",
                (lead_id, row["platform"], row["url"], row["url"]),
            )
        for contact in connection.execute(
            "SELECT id, full_name, normalized_name, job_title, department FROM contacts WHERE company_id = ?",
            (company_id,),
        ):
            cursor = connection.execute(
                "INSERT INTO domain_lead_contacts (domain_lead_id, full_name, normalized_name, job_title, department) VALUES (?, ?, ?, ?, ?)",
                (lead_id, contact["full_name"], contact["normalized_name"], contact["job_title"], contact["department"]),
            )
            lead_contact_id = int(cursor.lastrowid)
            for row in connection.execute("SELECT email FROM contact_emails WHERE contact_id = ?", (contact["id"],)):
                connection.execute(
                    "INSERT OR IGNORE INTO domain_lead_contact_emails (domain_lead_contact_id, email, normalized_email) VALUES (?, ?, ?)",
                    (lead_contact_id, row["email"], row["email"].lower()),
                )
            for row in connection.execute("SELECT phone FROM contact_phones WHERE contact_id = ?", (contact["id"],)):
                connection.execute(
                    "INSERT OR IGNORE INTO domain_lead_contact_phones (domain_lead_contact_id, phone, normalized_phone) VALUES (?, ?, ?)",
                    (lead_contact_id, row["phone"], row["phone"]),
                )
            for row in connection.execute("SELECT platform, url FROM contact_socials WHERE contact_id = ?", (contact["id"],)):
                connection.execute(
                    "INSERT INTO domain_lead_contact_socials (domain_lead_contact_id, platform, url, normalized_url) VALUES (?, ?, ?, ?)",
                    (lead_contact_id, row["platform"], row["url"], row["url"]),
                )
