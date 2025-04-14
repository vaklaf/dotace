import unittest
import sys

from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.library.utilities.strings import remove_czech_diacritics, clean_and_format_string

class TestStringUtilities(unittest.TestCase):
    def test_remove_czech_diacritics(self):
        czech_text = "Příliš žluťoučký kůň úpěl ďábelské ódy."
        expected_output = "Prilis zlutoucky kun upel dabelske ody."
        result = remove_czech_diacritics(czech_text)
        self.assertEqual(result, expected_output)

    def test_clean_and_format_string(self):
        text = "  Hello, World!  "
        expected_output = "Hello_World"
        result = clean_and_format_string(text)
        self.assertEqual(result, expected_output)
        
    def test_clean_and_format_string_with_special_characters(self):
        text = "  Hello! @World#  "
        expected_output = "Hello_World"
        result = clean_and_format_string(text)
        self.assertEqual(result, expected_output)
        
if __name__ == "__main__":
    unittest.main()