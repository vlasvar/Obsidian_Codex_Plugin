import unittest

from scripts.slugify import slugify_title


class SlugifyTests(unittest.TestCase):
    def test_slugify_normalizes_titles(self):
        self.assertEqual(slugify_title("Karpathy's LLM Wiki Pattern!"), "karpathy-s-llm-wiki-pattern")

    def test_slugify_urls_and_empty_values(self):
        self.assertEqual(slugify_title("https://example.com/Deep Dive?q=1"), "example-com-deep-dive-q-1")
        self.assertEqual(slugify_title("!!!"), "untitled")


if __name__ == "__main__":
    unittest.main()
