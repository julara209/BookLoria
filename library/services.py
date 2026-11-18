import csv
import unicodedata
from collections import Counter
from pathlib import Path

from django.conf import settings

DATA_FILE = Path(settings.BASE_DIR) / "data" / "biblioteca_montenegro.csv"
NO_AUTHOR = "Autor no registrado"
UNCLASSIFIED = "Sin clasificar"

GENRE_ALIASES = {
    "CUENTOS": "CUENTO",
    "NOEVELA DE ADULTOS": "NOVELA DE ADULTOS",
    "NOVEL DE ADULTOS": "NOVELA DE ADULTOS",
    "NOVELA DE AADULTOS": "NOVELA DE ADULTOS",
    "NOVELA DE ADULTO": "NOVELA DE ADULTOS",
    "NOVELA DE ADUNTOS": "NOVELA DE ADULTOS",
    "NOVELAS DE ADULTOS": "NOVELA DE ADULTOS",
    "NOVLA DE ADULTOS": "NOVELA DE ADULTOS",
}

GENRE_CATEGORIES = {
    # Literatura
    "ANTOLOGIA": "Literatura",
    "ANTOLOGIA DE LAS LITERARTURAS": "Literatura",
    "CLASICOS UNIVERSALES": "Literatura",
    "CONFERENCIAS SOBRE LA LITERATURA": "Literatura",
    "CUENTO": "Literatura",
    "CUENTO COLOMBIANO": "Literatura",
    "CUENTO EXAEQUO": "Literatura",
    "CUENTO Y POESIA": "Literatura",
    "ENSAYO": "Literatura",
    "ESCRITORES MONTENEGRINOS": "Literatura",
    "LITERATURA": "Literatura",
    "LITERATURA ORAL INDIGENA": "Literatura",
    "LITERATURA UNIVERSAL": "Literatura",
    "MITOS Y LEYENDAS /ADULTOS": "Literatura",
    "NOVELA": "Literatura",
    "NOVELA DE ADULTOS": "Literatura",
    "POESIA": "Literatura",
    "TRADICION ORAL": "Literatura",
    "TRADICIONES MITICO LITERARIAS": "Literatura",

    # Infantil y juvenil
    "ENCICLOPEDIA INFANTIL": "Infantil y juvenil",
    "INFANTIL": "Infantil y juvenil",
    "JUGANDO SE APRENDE": "Infantil y juvenil",
    "MITOS Y LEYENDAS /INFANTIL": "Infantil y juvenil",
    "NOVELA INFANTIL": "Infantil y juvenil",
    "POESIA /INFANTIL": "Infantil y juvenil",
    "TEATRO / INFANTIL": "Infantil y juvenil",

    # Álbumes
    "ALBUM": "Álbumes",

    # Accesibilidad
    "BRAILLE": "Braille",

    # Arte y cultura
    "700 ARTE RECREACION Y DEPORTE": "Arte y cultura",
    "ARTE RECREACION Y DEPORTE": "Arte y cultura",
    "DRAMARTURGIA": "Arte y cultura",
    "MANUALIDADES": "Arte y cultura",
    "ORIGAMI, PLASTILINA, FOMY GLOBOS": "Arte y cultura",
    "RED NACIONAL DRAMATURGIA": "Arte y cultura",
    "SOBRE ARTE": "Arte y cultura",
    "TEATRO": "Arte y cultura",

    # Ciencias y tecnología
    "600 TECNOLOGIA (CIENCIAS APLICADAS)": "Ciencias y tecnología",
    "CIENCIAS NUTURALES Y MATEMATICAS": "Ciencias y tecnología",
    "FACULTAD DE MEDICINA": "Ciencias y tecnología",

    # Ciencias sociales e historia
    "900 GEOGRAFIA E HISTORIA": "Ciencias sociales e historia",
    "900GEOGRAFIA E HISTORIA": "Ciencias sociales e historia",
    "990 GEOGRAFIA E HISTORIA": "Ciencias sociales e historia",
    "CIENCIA SOCIALES": "Ciencias sociales e historia",
    "CIENCIAS SOCIALES": "Ciencias sociales e historia",
    "CIENCIENCIAS SOCIALES": "Ciencias sociales e historia",
    "CIENIAS SOCIALES": "Ciencias sociales e historia",
    "SOCIALES": "Ciencias sociales e historia",

    # Educación y consulta
    "CARTILLA": "Educación y consulta",
    "MAGISTERIO": "Educación y consulta",
    "VALORES": "Educación y consulta",

    # Idiomas
    "INGLES": "Idiomas",
}


class DataFileError(Exception):
    """Raised when the library data file cannot be read."""


def _clean_author(value):
    value = (value or "").strip()
    if value in ("", "-"):
        return NO_AUTHOR
    return value


def _strip_accents(text):
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def _normalize_genre(value):
    value = " ".join(_strip_accents((value or "").upper()).split())
    if not value or value == "-":
        return "SIN CLASIFICAR"
    return GENRE_ALIASES.get(value, value)


def _categorize_genre(value):
    genre = _normalize_genre(value)
    return GENRE_CATEGORIES.get(genre, UNCLASSIFIED)


def _to_int(value):
    try:
        return int(float(str(value).strip()))
    except (ValueError, TypeError):
        return 0


def load_books(path=DATA_FILE):
    """Read the CSV and return a list of books as dictionaries."""
    try:
        with open(path, newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            return [
                {
                    "title": (row.get("NOMBRE DEL LIBRO") or "").strip(),
                    "author": _clean_author(row.get("AUTOR")),
                    "genre": _normalize_genre(row.get("GENERO")),
                    "category": _categorize_genre(row.get("GENERO")),
                    "copies": _to_int(row.get("NUMERO")),
                }
                for row in reader
            ]
    except FileNotFoundError:
        raise DataFileError(
            "No se encontró el archivo de datos. "
            "Verifique que exista data/biblioteca_montenegro.csv"
        )


def is_children_book(book):
    """True if the genre explicitly contains 'infantil'.

    The genre is already normalized (uppercase, no accents), so a plain
    substring check is enough. An ALBUM is NOT assumed to be a children's book.
    """
    return "INFANTIL" in book["genre"]


def filter_books(books, category="", only_children=False):
    """Filter books by reading category and, optionally, children's genres.

    'Sin clasificar' is hidden unless it is requested explicitly.
    """
    category = (category or "").strip()

    if category.casefold() == UNCLASSIFIED.casefold():
        results = [b for b in books if b["category"] == UNCLASSIFIED]
    elif category:
        results = [b for b in books if b["category"] == category]
    else:
        results = [b for b in books if b["category"] != UNCLASSIFIED]

    if only_children:
        results = [b for b in results if is_children_book(b)]

    return results


def get_categories(books):
    """Return reading categories with their book count (without 'Sin clasificar')."""
    counts = Counter(b["category"] for b in books if b["category"] != UNCLASSIFIED)
    return [
        {"name": name, "count": count}
        for name, count in sorted(
            counts.items(), key=lambda item: _strip_accents(item[0]).casefold()
        )
    ]


def count_unclassified(books):
    return sum(1 for b in books if b["category"] == UNCLASSIFIED)