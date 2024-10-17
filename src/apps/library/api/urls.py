from django.urls import path

from .views import author_detail_view
from .views import author_list_create_view
from .views import publisher_detail_view
from .views import publisher_list_create_view

urlpatterns_v1 = [
    path("v1/authors/", author_list_create_view, name="author-list-create"),
    path("v1/authors/<int:pk>/", author_detail_view, name="author-detail"),
    path(
        "v1/publishers/",
        publisher_list_create_view,
        name="publisher-list-create",
    ),
    path(
        "v1/publishers/<int:pk>/",
        publisher_detail_view,
        name="publisher-detail",
    ),
]

urlpatterns = urlpatterns_v1
