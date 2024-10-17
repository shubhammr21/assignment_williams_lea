from http import HTTPStatus

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from .factories import AuthorFactory
from .factories import BookFactory
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


@pytest.mark.django_db
class TestBookAPI:
    def test_list_books_with_pagination(self):
        author = AuthorFactory(name="Author 1")
        publisher = PublisherFactory(name="Publisher 1")
        BookFactory(title="Book 1", authors=[author], publisher=publisher)
        BookFactory(title="Book 2", authors=[author], publisher=publisher)

        response = client.get(reverse("book-list-create") + "?page_size=1")
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 1
        assert response.data["count"] == 2

    def test_filter_books_by_title(self):
        author = AuthorFactory(name="Author 1")
        publisher = PublisherFactory(name="Publisher 1")
        BookFactory(title="Book X", authors=[author], publisher=publisher)

        response = client.get(reverse("book-list-create") + "?title=X")
        assert response.status_code == HTTPStatus.OK
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == "Book X"

    def test_retrieve_book(self):
        author = AuthorFactory(name="Author 1")
        publisher = PublisherFactory(name="Publisher 1")
        book = BookFactory(title="Book 1", authors=[author], publisher=publisher)

        response = client.get(reverse("book-detail", kwargs={"pk": book.id}))
        assert response.status_code == HTTPStatus.OK
        assert response.data["title"] == "Book 1"

    def test_create_book(self):
        author = AuthorFactory()
        publisher = PublisherFactory()

        payload = {
            "title": "Book Title",
            "description": "Book Description",
            "author_ids": [author.id],
            "publisher_id": publisher.id,
        }
        response = client.post(reverse("book-list-create"), data=payload, format="json")
        assert response.status_code == HTTPStatus.CREATED
        assert response.data["title"] == "Book Title"

    def test_update_book(self):
        author = AuthorFactory(name="Author 1")
        publisher = PublisherFactory(name="Publisher 1")
        book = BookFactory(title="Book 1", authors=[author], publisher=publisher)
        data = {
            "title": "A Song of Ice and Fire",
            "description": "Fantasy novel series",
            "author_ids": [author.id],
            "publisher_id": publisher.id,
        }
        response = client.put(reverse("book-detail", kwargs={"pk": book.id}), data)
        assert response.status_code == HTTPStatus.OK
        assert response.data["title"] == "A Song of Ice and Fire"

    def test_partial_update_book(self):
        author = AuthorFactory(name="Author 1")
        publisher = PublisherFactory(name="Publisher 1")
        book = BookFactory(title="Book 1", authors=[author], publisher=publisher)
        data = {"description": "Book Description"}
        response = client.patch(reverse("book-detail", kwargs={"pk": book.id}), data)
        assert response.status_code == HTTPStatus.OK
        assert response.data["description"] == "Book Description"

    def test_delete_book(self):
        author = AuthorFactory(name="Author 1")
        publisher = PublisherFactory(name="Publisher 1")
        book = BookFactory(title="Book 1", authors=[author], publisher=publisher)
        response = client.delete(reverse("book-detail", kwargs={"pk": book.id}))
        assert response.status_code == HTTPStatus.NO_CONTENT
        # Confirm that the book was deleted
        response = client.get(reverse("book-detail", kwargs={"pk": book.id}))
        assert response.status_code == HTTPStatus.NOT_FOUND
