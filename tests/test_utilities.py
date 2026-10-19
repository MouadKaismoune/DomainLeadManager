from app.core.utilities import extract_extension, normalize_domain
import unittest


class UtilityTests(unittest.TestCase):
    def test_normalize_domain_removes_protocol_www_and_trailing_dot(self):
        self.assertEqual(normalize_domain("https://www.Example.com/"), "example.com")

    def test_extract_extension(self):
        self.assertEqual(extract_extension("example.com"), "com")
