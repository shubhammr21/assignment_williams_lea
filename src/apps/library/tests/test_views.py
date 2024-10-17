from http import HTTPStatus

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .factories import AuthorFactory

client = APIClient()


@pytest.mark.django_db
class TestAuthorAPI:
    def test_list_authors(self):
        authors = [AuthorFactory(name=f"Author {i}") for i in range(1, 5)]

        response = client.get(reverse("author-list-create"))
        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == len(authors)

    def test_create_author(self):
        payload = {
            "name": "Author's Name",
            "bio": "Author's Bio...",
        }
        response = client.post(
            reverse("author-list-create"),
            data=payload,
            format="json",
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["name"] == "Author's Name"

    def test_list_authors_with_pagination(self):
        authors = [AuthorFactory(name=f"Author {i}") for i in range(1, 5)]

        response = client.get(reverse("author-list-create") + "?page_size=2")
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 2
        assert response.data["count"] == len(authors)

    def test_filter_authors_by_name(self):
        AuthorFactory(name="Author X")
        AuthorFactory(name="Author Y")

        response = client.get(reverse("author-list-create") + "?name=X")
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Author X"
