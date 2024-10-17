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
            "name": "Tolkien",
            "bio": "Author of The Hobbit and Lord of the Rings.",
        }
        response = client.post(
            reverse("author-list-create"),
            data=payload,
            format="json",
        )
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["name"] == "Tolkien"
