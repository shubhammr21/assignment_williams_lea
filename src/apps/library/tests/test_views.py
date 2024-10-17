from http import HTTPStatus

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .factories import AuthorFactory
from .factories import PublisherFactory

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


@pytest.mark.django_db
class TestPublisherAPI:
    def test_list_publishers_with_pagination(self):
        PublisherFactory(name="Author 1")
        PublisherFactory(name="Author 2")
        PublisherFactory(name="Author 3")

        response = client.get(reverse("publisher-list-create") + "?page_size=2")
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 2
        assert response.data["count"] == 3

    def test_filter_publishers_by_name(self):
        PublisherFactory(name="Author X")
        PublisherFactory(name="Author Y")

        response = client.get(reverse("publisher-list-create") + "?name=X")
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["name"] == "Author X"

    def test_retrieve_publisher(self):
        publisher = PublisherFactory(name="Author 1")
        response = client.get(reverse("publisher-detail", kwargs={"pk": publisher.id}))
        assert response.status_code == HTTPStatus.OK
        assert response.data["name"] == "Author 1"

    def test_update_publisher(self):
        publisher = PublisherFactory(name="Author 1")
        data = {"name": "Penguin Author 3", "website": "http://example.com"}
        response = client.put(
            reverse("publisher-detail", kwargs={"pk": publisher.id}),
            data,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data["name"] == "Penguin Author 3"

    def test_partial_update_publisher(self):
        publisher = PublisherFactory(name="Author 1")
        data = {"website": "http://example.com"}
        response = client.patch(
            reverse("publisher-detail", kwargs={"pk": publisher.id}),
            data,
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data["website"] == "http://example.com"

    def test_delete_publisher(self):
        publisher = PublisherFactory(name="Author 1")
        response = client.delete(
            reverse("publisher-detail", kwargs={"pk": publisher.id}),
        )
        assert response.status_code == HTTPStatus.NO_CONTENT
        # Confirm that the publisher was deleted
        response = client.get(reverse("publisher-detail", kwargs={"pk": publisher.id}))
        assert response.status_code == HTTPStatus.NOT_FOUND
