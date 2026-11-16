import csv
import unicodedata
from pathlib import Path

from django.conf import settings

DATA_FILE = Path(settings.BASE_DIR) / "data" / "biblioteca_montenegro.csv"
NO_AUTHOR = "Autor no registrado"

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


def _to_int(value):
    try:
        return int(float(str(value).strip()))
    except ValueError:
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
                    "copies": _to_int(row.get("NUMERO")),
                }
                for row in reader
            ]
    except FileNotFoundError:
        raise DataFileError(
            "No se encontró el archivo de datos. "
            "Verifique que exista data/biblioteca_montenegro.csv"
        )