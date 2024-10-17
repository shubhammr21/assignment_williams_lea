import pytest

from ..models import Author
from ..models import Book
from ..models import Publisher
from ..services import AuthorService
from ..services import BookService
from ..services import PublisherService
from .factories import AuthorFactory
from .factories import BookFactory
from .factories import PublisherFactory


@pytest.mark.django_db
class TestAuthorService:
    def test_list_authors(self):
        batch = 3

        authors = AuthorFactory.create_batch(batch)

        result = AuthorService.list_authors()

        assert len(result) == batch
        assert list(result) == authors

    def test_get_author_by_id(self):
        author = AuthorFactory()

        result = AuthorService.get_author_by_id(author.id)

        assert result == author

    def test_get_author_by_id_invalid(self):
        with pytest.raises(Author.DoesNotExist):
            AuthorService.get_author_by_id(9999)


@pytest.mark.django_db
class TestPublisherService:
    def test_list_publishers(self):
        batch = 3

        publishers = PublisherFactory.create_batch(batch)

        result = PublisherService.list_publishers()

        assert len(result) == batch
        assert list(result) == publishers

    def test_get_publisher_by_id(self):
        publisher = PublisherFactory()

        result = PublisherService.get_publisher_by_id(publisher.id)

        assert result == publisher

    def test_get_publisher_by_id_invalid(self):
        with pytest.raises(Publisher.DoesNotExist):
            PublisherService.get_publisher_by_id(9999)


@pytest.mark.django_db
class TestBookService:
    def test_list_books(self):
        batch = 3
        books = BookFactory.create_batch(batch)

        result = BookService.list_books()

        assert len(result) == batch
        assert list(result) == books

    def test_get_book_by_id(self):
        book = BookFactory()

        result = BookService.get_book_by_id(book.id)

        assert result == book

    def test_get_book_by_id_invalid(self):
        with pytest.raises(Book.DoesNotExist):
            BookService.get_book_by_id(9999)

    def test_get_books_by_status(self):
        batch = 2

        books_published = BookFactory.create_batch(batch, status="published")
        books_draft = BookFactory.create_batch(batch, status="draft")

        published_books = BookService.get_books_by_status("published")
        draft_books = BookService.get_books_by_status("draft")

        assert len(published_books) == batch
        assert list(published_books) == books_published
        assert len(draft_books) == batch
        assert list(draft_books) == books_draft

    def test_get_books_by_invalid_status(self):
        result = BookService.get_books_by_status("nonexistent_status")

        assert len(result) == 0
