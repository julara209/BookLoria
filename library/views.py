from django.core.paginator import Paginator
from django.shortcuts import render

from .services import DataFileError, get_categories, load_books, search_books

BOOKS_PER_PAGE = 12


def _inventory():
    """All books from the CSV, ignoring rows without a title."""
    return [book for book in load_books() if book["title"]]


def home(request):
    return render(request, "library/index.html")


def category_list(request):
    """HU_001: show the reading categories."""
    try:
        categories = get_categories(_inventory())
    except DataFileError as error:
        return render(request, "library/categories.html", {"error": str(error)}, status=500)
    return render(request, "library/categories.html", {"categories": categories})


def book_list(request):
    """HU_001 and HU_002: inventory, optionally filtered by category and search."""
    genre = request.GET.get("categoria", "").strip()
    query = request.GET.get("q", "").strip()
    try:
        all_books = _inventory()
    except DataFileError as error:
        return render(request, "library/books.html", {"error": str(error)}, status=500)

    results = search_books(all_books, genre, query)
    page = Paginator(results, BOOKS_PER_PAGE).get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)

    context = {
        "page": page,
        "genre": genre,
        "query": query,
        "total": len(results),
        "inventory_empty": not all_books,
        "querystring": params.urlencode(),
    }
    return render(request, "library/books.html", context)