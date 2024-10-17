import pytest

from ..repositories import AuthorRepository
from ..repositories import BookRepository
from ..repositories import PublisherRepository
from .factories import AuthorFactory
from .factories import BookFactory
from .factories import PublisherFactory


@pytest.mark.django_db
class TestAuthorRepository:
    def test_get_all(self):
        AuthorFactory(name="Author 1")
        repo = AuthorRepository()
        assert len(repo.get_all()) == 1

    def test_get_by_id(self):
        author = AuthorFactory(name="Author 1")
        repo = AuthorRepository()
        fetched_author = repo.get_by_id(author.id)
        assert fetched_author.name == "Author 1"


@pytest.mark.django_db
class TestPublisherRepository:
    def test_get_all(self):
        PublisherFactory(name="Publisher 1")
        assert len(PublisherRepository.get_all()) == 1

    def test_get_by_id(self):
        publisher = PublisherFactory(name="Publisher 2")
        fetched_publisher = PublisherRepository.get_by_id(publisher.id)
        assert fetched_publisher.name == "Publisher 2"


@pytest.mark.django_db
class TestBookRepository:
    def test_get_all(self):
        publisher = PublisherFactory(name="Publisher")
        BookFactory(title="Book 1", publisher=publisher)
        assert len(BookRepository.get_all()) == 1

    def test_get_by_id(self):
        publisher = PublisherFactory(name="Publisher")
        book = BookFactory(title="Book 2", publisher=publisher)
        fetched_book = BookRepository.get_by_id(book.id)
        assert fetched_book.title == "Book 2"
