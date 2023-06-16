from djbackoffice.core import backoffice, BackofficeOptions
from .models import Book


class BookBackoffice(BackofficeOptions):
    icon_menu = "bi-book"
    search_fields = ("title", "author__name")


backoffice.register(Book, BookBackoffice)
