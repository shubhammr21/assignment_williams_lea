from rest_framework.generics import ListCreateAPIView

from src.apps.utils.pagination import StandardPageNumberPagination

from ..models import Author
from .serializers import AuthorSerializer


class AuthorListCreateView(ListCreateAPIView):
    pagination_class = StandardPageNumberPagination
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return Author.objects.all()


author_list_create_view = AuthorListCreateView.as_view()
