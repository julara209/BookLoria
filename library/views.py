from django.core.paginator import Paginator
from django.shortcuts import render

from .services import (
    UNCLASSIFIED,
    DataFileError,
    count_unclassified,
    filter_books,
    get_categories,
    load_books,
)

HOME_BOOKS = 50
BOOKS_PER_PAGE = 50


def _inventory():
    """All books from the CSV, ignoring rows without a title."""
    return [book for book in load_books() if book["title"]]


def home(request):
    """Issue #3: first books of the inventory, with the data source."""
    try:
        books = _inventory()
    except DataFileError as error:
        return render(request, "library/index.html", {"error": str(error)}, status=500)
    context = {
        "books": books[:HOME_BOOKS],
        "total": len(books),
        "shown": min(HOME_BOOKS, len(books)),
    }
    return render(request, "library/index.html", context)


def book_list(request):
    """Issue #6: choose a reading category and see its books."""
    category = request.GET.get("categoria", "").strip()
    try:
        all_books = _inventory()
    except DataFileError as error:
        return render(request, "library/books.html", {"error": str(error)}, status=500)

    results = filter_books(all_books, category)
    page = Paginator(results, BOOKS_PER_PAGE).get_page(request.GET.get("page"))

    params = request.GET.copy()
    params.pop("page", None)

    context = {
        "categories": get_categories(all_books),
        "selected": category,
        "showing_unclassified": category.casefold() == UNCLASSIFIED.casefold(),
        "unclassified_count": count_unclassified(all_books),
        "unclassified_name": UNCLASSIFIED,
        "page": page,
        "total": len(results),
        "querystring": params.urlencode(),
    }
    return render(request, "library/books.html", context)