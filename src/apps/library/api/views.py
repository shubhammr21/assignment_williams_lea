from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from src.apps.utils.pagination import StandardPageNumberPagination

from ..filters import AuthorFilter
from ..filters import BookFilter
from ..filters import PublisherFilter
from ..services import AuthorService
from ..services import BookService
from ..services import PublisherService
from .serializers import AuthorSerializer
from .serializers import BookSerializer
from .serializers import PublisherSerializer


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


class PublisherListCreateView(ListCreateAPIView):
    pagination_class = StandardPageNumberPagination
    serializer_class = PublisherSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PublisherFilter

    def get_queryset(self):
        return PublisherService.list_publishers()


publisher_list_create_view = PublisherListCreateView.as_view()


class PublisherDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PublisherSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return PublisherService.list_publishers()


publisher_detail_view = PublisherDetailView.as_view()


class BookListCreateView(ListCreateAPIView):
    pagination_class = StandardPageNumberPagination
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_queryset(self):
        return BookService.list_books()


book_list_create_view = BookListCreateView.as_view()


class BookDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return BookService.list_books()


book_detail_view = BookDetailView.as_view()
