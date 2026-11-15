from django.test import SimpleTestCase

from library.services import NO_AUTHOR, _clean_author, load_books


class LoadBooksTests(SimpleTestCase):
    def test_loads_all_records(self):
        self.assertEqual(len(load_books()), 4162)

    def test_missing_author_becomes_placeholder(self):
        self.assertEqual(_clean_author("-"), NO_AUTHOR)
        self.assertEqual(_clean_author(""), NO_AUTHOR)
        self.assertEqual(_clean_author(None), NO_AUTHOR)