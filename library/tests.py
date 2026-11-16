
from django.test import SimpleTestCase

from library.services import NO_AUTHOR, _clean_author, _normalize_genre, load_books


class LoadBooksTests(SimpleTestCase):

    def test_loads_all_records(self):
        self.assertEqual(len(load_books()), 4162)

    def test_missing_author_becomes_placeholder(self):
        self.assertEqual(_clean_author("-"), NO_AUTHOR)
        self.assertEqual(_clean_author(""), NO_AUTHOR)
        self.assertEqual(_clean_author(None), NO_AUTHOR)


class NormalizeGenreTests(SimpleTestCase):

    def test_normalizes_uppercase_and_spaces(self):
        self.assertEqual(_normalize_genre("  cuento  "), "CUENTO")

    def test_unifies_cuento_and_cuentos(self):
        self.assertEqual(_normalize_genre("CUENTOS"), "CUENTO")

    def test_corrects_novela_variants(self):
        self.assertEqual(
            _normalize_genre("NOVELA DE AADULTOS"),
            "NOVELA DE ADULTOS"
        )

    def test_empty_genre_becomes_unclassified(self):
        self.assertEqual(_normalize_genre("-"), "SIN CLASIFICAR")
        self.assertEqual(_normalize_genre(""), "SIN CLASIFICAR")
        self.assertEqual(_normalize_genre(None), "SIN CLASIFICAR")
