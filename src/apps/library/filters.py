from django_filters import CharFilter
from django_filters import FilterSet

from .models import Author
from .models import Book
from .models import Publisher


class AuthorFilter(FilterSet):
    name = CharFilter(
        lookup_expr="icontains",
    )

    class Meta:
        model = Author
        fields = ["name"]


class PublisherFilter(FilterSet):
    name = CharFilter(
        lookup_expr="icontains",
    )

    class Meta:
        model = Publisher
        fields = ["name"]


class BookFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    authors = CharFilter(
        field_name="authors__name",
        lookup_expr="icontains",
    )
    publisher = CharFilter(
        field_name="publisher__name",
        lookup_expr="icontains",
    )

    class Meta:
        model = Book
        fields = [
            "title",
            "authors",
            "publisher",
            "status",
        ]
