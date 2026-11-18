from unittest.mock import patch

from django.test import SimpleTestCase

from library.services import (
    GENRE_CATEGORIES,
    NO_AUTHOR,
    DataFileError,
    _categorize_genre,
    _clean_author,
    _normalize_genre,
    load_books,
)

VALID_CATEGORIES = set(GENRE_CATEGORIES.values()) | {"Sin clasificar"}


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
            "NOVELA DE ADUÑTOS", "NOVELAS DE ADULTOS",
            "NOVLA DE ADULTOS",
        ]
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertEqual(
                    _normalize_genre(variant),
                    "NOVELA DE ADULTOS",
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
        self.assertEqual(_categorize_genre("NOVELA DE ADULTOS"), "Literatura")

    def test_infantil_genres_receive_correct_category(self):
        self.assertEqual(_categorize_genre("NOVELA INFANTIL"), "Infantil")
        self.assertEqual(_categorize_genre("POESIA /INFANTIL"), "Infantil")

    def test_art_genres_receive_correct_category(self):
        self.assertEqual(_categorize_genre("TEATRO"), "Arte y cultura")

    def test_accented_genre_is_categorized(self):
        self.assertEqual(_categorize_genre("POESÍA"), "Literatura")

    def test_album_and_braille_have_their_own_category(self):
        self.assertEqual(_categorize_genre("ALBUM"), "Álbumes")
        self.assertEqual(_categorize_genre("BRAILLE"), "Braille")

    def test_unknown_genre_is_unclassified(self):
        self.assertEqual(
            _categorize_genre("GENERO DESCONOCIDO"),
            "Sin clasificar",
        )

    def test_every_book_has_a_valid_category(self):
        for book in load_books():
            self.assertIn(book["category"], VALID_CATEGORIES)

    def test_infantil_category_matches_infantil_genre(self):
        books = load_books()
        by_category = [b for b in books if b["category"] == "Infantil"]
        by_genre = [b for b in books if "INFANTIL" in b["genre"]]
        self.assertEqual(len(by_category), len(by_genre))
        self.assertEqual(len(by_category), 271)


class HomeViewTests(SimpleTestCase):

    def test_home_loads_and_lists_50_books(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["books"]), 50)
        self.assertEqual(response.context["total"], 4162)

    def test_home_shows_title_author_and_copies_headers(self):
        response = self.client.get("/")
        for header in ("Título", "Autor", "Ejemplares"):
            self.assertContains(response, header)

    def test_home_cites_the_data_source(self):
        html = self.client.get("/").content.decode()
        self.assertIn("hecw-3dai", html)
        self.assertIn("datos.gov.co", html)
        self.assertIn("no indica si un libro está disponible hoy", html)

    def test_home_shows_placeholder_for_book_without_author(self):
        books = [{
            "title": "Libro de prueba",
            "author": NO_AUTHOR,
            "genre": "CUENTO",
            "category": "Literatura",
            "copies": 1,
        }]
        with patch("library.views.load_books", return_value=books):
            response = self.client.get("/")
        self.assertContains(response, "Autor no registrado")

    def test_home_does_not_break_if_data_file_is_missing(self):
        error = DataFileError("falta el archivo")
        with patch("library.views.load_books", side_effect=error):
            response = self.client.get("/")
        self.assertContains(response, "falta el archivo", status_code=500)