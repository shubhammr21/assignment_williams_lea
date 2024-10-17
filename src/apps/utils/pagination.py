from rest_framework.pagination import CursorPagination
from rest_framework.pagination import PageNumberPagination


class StandardPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class StandardCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = "page_size"
