from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from src.apps.utils.pagination import StandardPageNumberPagination

from ..filters import AuthorFilter
from ..services import AuthorService
from .serializers import AuthorSerializer


class AuthorListCreateView(ListCreateAPIView):
    pagination_class = StandardPageNumberPagination
    serializer_class = AuthorSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = AuthorFilter

    def get_queryset(self):
        return AuthorService.list_authors()


author_list_create_view = AuthorListCreateView.as_view()


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return AuthorService.list_authors()


author_detail_view = AuthorDetailView.as_view()
