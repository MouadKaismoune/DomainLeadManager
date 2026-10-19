import unittest

from app.ui.theme import PALETTES, build_stylesheet


class ThemeTests(unittest.TestCase):
    def test_each_mode_builds_a_complete_stylesheet(self):
        for mode, palette in PALETTES.items():
            with self.subTest(mode=mode):
                stylesheet = build_stylesheet(mode)
                self.assertNotIn("$", stylesheet)
                self.assertIn(palette["bg"], stylesheet)
                self.assertIn("#appHeader", stylesheet)
                self.assertIn("#appFooter", stylesheet)

    def test_unknown_mode_falls_back_to_light(self):
        self.assertEqual(build_stylesheet("unknown"), build_stylesheet("light"))


if __name__ == "__main__":
    unittest.main()
