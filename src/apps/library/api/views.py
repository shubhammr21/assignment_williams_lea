from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView

from src.apps.utils.pagination import StandardPageNumberPagination

from ..filters import AuthorFilter
from ..models import Author
from .serializers import AuthorSerializer


class AuthorListCreateView(ListCreateAPIView):
    pagination_class = StandardPageNumberPagination
    serializer_class = AuthorSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter

    def get_queryset(self):
        return Author.objects.all()


author_list_create_view = AuthorListCreateView.as_view()
