import unittest

from app.ui.table_data import (
    aggregate_contact_rows,
    aggregate_overview_rows,
    display_value,
)


class TableDataTests(unittest.TestCase):
    def test_overview_collapses_company_and_contact_email_combinations(self):
        rows = [
            {
                "lead_id": 1,
                "contact_id": 10,
                "company_name": "Acme",
                "company_email": "hello@acme.test",
                "contact_name": "Sam",
                "contact_email": "sam@acme.test",
            },
            {
                "lead_id": 1,
                "contact_id": 10,
                "company_name": "Acme",
                "company_email": "sales@acme.test",
                "contact_name": "Sam",
                "contact_email": "sam@acme.test",
            },
            {
                "lead_id": 1,
                "contact_id": 10,
                "company_name": "Acme",
                "company_email": "hello@acme.test",
                "contact_name": "Sam",
                "contact_email": "sam@work.test",
            },
        ]

        result = aggregate_overview_rows(rows)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["company_email"], "hello@acme.test, sales@acme.test")
        self.assertEqual(result[0]["contact_email"], "sam@acme.test, sam@work.test")

    def test_overview_keeps_one_row_per_contact(self):
        rows = [
            {"lead_id": 1, "contact_id": 10, "company_name": "Acme"},
            {"lead_id": 1, "contact_id": 11, "company_name": "Acme"},
            {"lead_id": 2, "contact_id": None, "company_name": "Beta"},
        ]

        result = aggregate_overview_rows(rows)

        self.assertEqual(len(result), 3)
        self.assertEqual([row["lead_id"] for row in result], [1, 1, 2])

    def test_contact_rows_join_emails_without_duplicates(self):
        rows = [
            {
                "id": 10,
                "full_name": "Sam",
                "company_name": "Acme",
                "email": "sam@acme.test",
            },
            {
                "id": 10,
                "full_name": "Sam",
                "company_name": "Acme",
                "email": "sam@work.test",
            },
            {
                "id": 10,
                "full_name": "Sam",
                "company_name": "Acme",
                "email": "sam@acme.test",
            },
        ]

        result = aggregate_contact_rows(rows)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["email"], "sam@acme.test, sam@work.test")

    def test_display_value_hides_empty_values(self):
        self.assertEqual(display_value(None), "—")
        self.assertEqual(display_value("   "), "—")
        self.assertEqual(display_value("Acme"), "Acme")


if __name__ == "__main__":
    unittest.main()
