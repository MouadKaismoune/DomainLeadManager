import tempfile
import unittest
from pathlib import Path

from app.database import connection
from app.services.domain_service import DomainService
from app.services.workspace_service import WorkspaceService


class DomainWorkspaceTests(unittest.TestCase):
    def test_workspace_data_is_scoped_to_selected_domain(self):
        original_data_dir = connection.DATA_DIR
        original_database_path = connection.DATABASE_PATH
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            connection.DATA_DIR = directory_path
            connection.DATABASE_PATH = directory_path / "test.db"
            try:
                connection.initialize_database()
                domain_service = DomainService()
                first_domain = domain_service.create_domain("first.example")
                second_domain = domain_service.create_domain("second.example")
                workspace = WorkspaceService()

                workspace.add_prospect(
                    first_domain,
                    {
                        "company": {"name": "Same Company", "website": "", "description": "", "address": "", "city": "", "state": "", "country": ""},
                        "company_emails": [],
                        "company_phones": [],
                        "company_socials": [],
                        "contacts": [{"name": "Jane Smith", "job_title": "", "department": "", "emails": ["jane@example.com", "jane.work@example.com"], "phones": [], "socials": []}],
                        "priority": "normal",
                        "notes": "First domain note",
                    },
                )
                workspace.add_prospect(
                    second_domain,
                    {
                        "company": {"name": "Same Company", "website": "", "description": "", "address": "", "city": "", "state": "", "country": ""},
                        "company_emails": [],
                        "company_phones": [],
                        "company_socials": [],
                        "contacts": [{"name": "Jane Smith", "job_title": "", "department": "", "emails": ["jane@example.com"], "phones": [], "socials": []}],
                        "priority": "high",
                        "notes": "Second domain note",
                    },
                )

                first_rows = workspace.list_domain_workspace(first_domain)
                second_rows = workspace.list_domain_workspace(second_domain)
                first_contacts = workspace.list_domain_contacts(first_domain)
                self.assertEqual(len(first_rows), 2)
                self.assertEqual(len(second_rows), 1)
                self.assertEqual(len(first_contacts), 2)
                self.assertEqual(
                    {contact["email"] for contact in first_contacts},
                    {"jane@example.com", "jane.work@example.com"},
                )
                self.assertEqual(first_rows[0]["notes"], "First domain note")
                self.assertEqual(second_rows[0]["notes"], "Second domain note")
            finally:
                connection.DATA_DIR = original_data_dir
                connection.DATABASE_PATH = original_database_path
