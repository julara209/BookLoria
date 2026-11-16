
from django.test import SimpleTestCase

from library.services import (
    NO_AUTHOR,
    _clean_author,
    _normalize_genre,
    _categorize_genre,
    load_books,
)


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

    def test_removes_accents(self):
        self.assertEqual(_normalize_genre("poesía"), "POESIA")
        self.assertEqual(_normalize_genre("CUENTO Y POESÍA"), "CUENTO Y POESIA")

    def test_unifies_cuento_and_cuentos(self):
        self.assertEqual(_normalize_genre("CUENTOS"), "CUENTO")

    def test_all_novela_variants_are_unified(self):
        variants = [
            "NOEVELA DE ADULTOS", "NOVEL DE ADULTOS",
            "NOVELA DE AADULTOS", "NOVELA DE ADULTO",
            "NOVELA DE ADUNTOS", "NOVELAS DE ADULTOS",
            "NOVLA DE ADULTOS",
        ]
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertEqual(
                    _normalize_genre(variant),
                    "NOVELA DE ADULTOS"
                )

    def test_empty_genre_becomes_unclassified(self):
        self.assertEqual(_normalize_genre("-"), "SIN CLASIFICAR")
        self.assertEqual(_normalize_genre(""), "SIN CLASIFICAR")
        self.assertEqual(_normalize_genre(None), "SIN CLASIFICAR")

    def test_infantil_is_preserved(self):
        infantil = [b for b in load_books() if "INFANTIL" in b["genre"]]
        self.assertEqual(len(infantil), 271)


class GenreCategoriesTests(SimpleTestCase):

    def test_literature_genres_receive_correct_category(self):
        self.assertEqual(
            _categorize_genre("NOVELA DE ADULTOS"),
            "Literatura"
        )

    def test_infantil_genres_receive_correct_category(self):
        self.assertEqual(
            _categorize_genre("NOVELA INFANTIL"),
            "Infantil y juvenil"
        )

    def test_art_genres_receive_correct_category(self):
        self.assertEqual(
            _categorize_genre("TEATRO"),
            "Arte y cultura"
        )

    def test_unknown_genre_is_unclassified(self):
        self.assertEqual(
            _categorize_genre("GENERO DESCONOCIDO"),
            "Sin clasificar"
        )

    def test_every_book_has_exactly_one_category(self):
        for book in load_books():
            self.assertIn("category", book)
            self.assertTrue(book["category"])
