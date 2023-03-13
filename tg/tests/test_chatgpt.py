import unittest
from tg.chatgpt.utils import contains_delimiter


class TestContainsDelimiter(unittest.TestCase):
    def test_with_delimiter(self):
        self.assertTrue(contains_delimiter("Hello, world! "))
        self.assertTrue(contains_delimiter("This is a sentence. "))
        self.assertTrue(contains_delimiter("How are you? "))
        self.assertTrue(contains_delimiter("I'm fine. "))
        self.assertTrue(contains_delimiter("Testing... testing... 1, 2, 3. "))

    def test_without_delimiter(self):
        self.assertFalse(contains_delimiter(""))
        self.assertFalse(contains_delimiter("This is a sentence"))
        self.assertFalse(contains_delimiter("How are you"))
        self.assertFalse(contains_delimiter("I'm fine"))
        self.assertFalse(contains_delimiter("Testing testing 1 2 3"))


if __name__ == "__main__":
    unittest.main()
