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

    def test_retrieve_author(self):
        author = AuthorFactory(name="Author 1")
        response = client.get(reverse("author-detail", kwargs={"pk": author.id}))
        assert response.status_code == HTTPStatus.OK
        assert response.data["name"] == "Author 1"

    def test_update_author(self):
        author = AuthorFactory(name="Author 1")
        data = {"name": "Author", "bio": "Bio"}
        response = client.put(reverse("author-detail", kwargs={"pk": author.id}), data)
        assert response.status_code == HTTPStatus.OK
        assert response.data["name"] == "Author"

    def test_partial_update_author(self):
        author = AuthorFactory(name="Author 1")
        data = {"bio": "British author"}
        response = client.patch(
            reverse("author-detail", kwargs={"pk": author.id}),
            data,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data["bio"] == "British author"

    def test_delete_author(self):
        author = AuthorFactory(name="Author 1")
        response = client.delete(reverse("author-detail", kwargs={"pk": author.id}))
        assert response.status_code == HTTPStatus.NO_CONTENT
        # Confirm that the author was deleted
        response = client.get(reverse("author-detail", kwargs={"pk": author.id}))
        assert response.status_code == HTTPStatus.NOT_FOUND
