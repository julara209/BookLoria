from unittest.mock import patch

from django.test import SimpleTestCase

from library.services import (
    GENRE_CATEGORIES,
    NO_AUTHOR,
    DataFileError,
    _categorize_genre,
    _clean_author,
    _normalize_genre,
    count_unclassified,
    filter_books,
    get_categories,
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


def _book(title="Libro", author="Autora", genre="CUENTO", category="Literatura", copies=1):
    return {
        "title": title,
        "author": author,
        "genre": genre,
        "category": category,
        "copies": copies,
    }


class FilterBooksTests(SimpleTestCase):

    def setUp(self):
        self.books = [
            _book("A", genre="CUENTO", category="Literatura"),
            _book("B", genre="NOVELA INFANTIL", category="Infantil"),
            _book("C", genre="TEATRO", category="Arte y cultura"),
            _book("D", genre="SIN CLASIFICAR", category="Sin clasificar"),
        ]

    def test_category_filter_returns_only_that_category(self):
        result = filter_books(self.books, "Arte y cultura")
        self.assertEqual([b["title"] for b in result], ["C"])

    def test_category_without_results_returns_empty_list(self):
        self.assertEqual(filter_books(self.books, "Idiomas"), [])

    def test_unclassified_is_hidden_by_default(self):
        titles = [b["title"] for b in filter_books(self.books)]
        self.assertNotIn("D", titles)
        self.assertEqual(titles, ["A", "B", "C"])

    def test_unclassified_is_shown_when_requested(self):
        result = filter_books(self.books, "Sin clasificar")
        self.assertEqual([b["title"] for b in result], ["D"])

    def test_categories_do_not_include_unclassified(self):
        names = [c["name"] for c in get_categories(self.books)]
        self.assertNotIn("Sin clasificar", names)
        self.assertEqual(count_unclassified(self.books), 1)


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

    def test_home_links_to_the_category_page(self):
        self.assertContains(self.client.get("/"), 'href="/libros/"')

    def test_home_shows_placeholder_for_book_without_author(self):
        books = [_book("Libro de prueba", author=NO_AUTHOR)]
        with patch("library.views.load_books", return_value=books):
            response = self.client.get("/")
        self.assertContains(response, "Autor no registrado")

    def test_home_does_not_break_if_data_file_is_missing(self):
        error = DataFileError("falta el archivo")
        with patch("library.views.load_books", side_effect=error):
            response = self.client.get("/")
        self.assertContains(response, "falta el archivo", status_code=500)


class BookListViewTests(SimpleTestCase):

    def test_page_has_selector_with_categories(self):
        html = self.client.get("/libros/").content.decode()
        self.assertIn("<select", html)
        for name in ("Literatura", "Infantil", "Álbumes", "Braille"):
            self.assertIn(name, html)

    def test_unclassified_is_not_an_option_and_page_warns(self):
        html = self.client.get("/libros/").content.decode()
        self.assertNotIn('<option value="Sin clasificar"', html)
        self.assertIn("no se muestran por defecto", html)

    def test_choosing_a_category_shows_title_author_and_copies(self):
        response = self.client.get("/libros/?categoria=Idiomas")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 1)
        for header in ("Título", "Autor", "Ejemplares"):
            self.assertContains(response, header)

    def test_category_with_records_lists_only_that_category(self):
        response = self.client.get("/libros/?categoria=Braille")
        self.assertEqual(response.context["total"], 40)
        for book in response.context["page"]:
            self.assertEqual(book["category"], "Braille")

    def test_category_without_results_shows_clear_message(self):
        html = self.client.get("/libros/?categoria=Inexistente").content.decode()
        self.assertIn("No hay libros que coincidan", html)

    def test_book_without_author_shows_placeholder(self):
        books = [_book("Libro de prueba", author=NO_AUTHOR)]
        with patch("library.views.load_books", return_value=books):
            response = self.client.get("/libros/?categoria=Literatura")
        self.assertContains(response, "Autor no registrado")

    def test_unclassified_can_be_requested_explicitly(self):
        response = self.client.get("/libros/?categoria=Sin+clasificar")
        self.assertEqual(response.context["total"], count_unclassified(load_books()))
        self.assertGreater(response.context["total"], 0)
        self.assertIn("no tienen categoría de lectura", response.content.decode())

    def test_pagination_keeps_the_selected_category(self):
        html = self.client.get("/libros/?categoria=Literatura&page=2").content.decode()
        self.assertIn("categoria=Literatura&amp;page=3", html)

    def test_book_list_does_not_break_if_data_file_is_missing(self):
        error = DataFileError("falta el archivo")
        with patch("library.views.load_books", side_effect=error):
            response = self.client.get("/libros/")
        self.assertContains(response, "falta el archivo", status_code=500)