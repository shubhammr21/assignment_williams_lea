from django_filters import CharFilter
from django_filters import FilterSet

from .models import Author


class AuthorFilter(FilterSet):
    name = CharFilter(
        lookup_expr="icontains",
    )

    class Meta:
        model = Author
        fields = ["name"]
