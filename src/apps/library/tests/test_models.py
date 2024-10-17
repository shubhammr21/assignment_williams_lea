# tests/test_models.py
import pytest
from django.core.exceptions import ValidationError

from .factories import AuthorFactory
from .factories import BookFactory
from .factories import PublisherFactory


@pytest.mark.django_db
class TestAuthorModel:
    def test_author_creation(self):
        author = AuthorFactory(name="J.K. Rowling")
        assert author.name == "J.K. Rowling"
        assert author.bio is not None

    def test_author_name_min_length_validation(self):
        author = AuthorFactory.build(name="Al")  # build doesn't save the object
        with pytest.raises(ValidationError) as excinfo:
            author.full_clean()  # full_clean will trigger model validations
        assert "Author name must be at least 3 characters long." in str(excinfo.value)


@pytest.mark.django_db
class TestPublisherModel:
    def test_publisher_creation(self):
        publisher = PublisherFactory(name="Penguin Books")
        assert publisher.name == "Penguin Books"
        assert publisher.website is not None


@pytest.mark.django_db
class TestBookModel:
    def test_book_creation(self):
        authors = [AuthorFactory() for _ in range(2)]
        publisher = PublisherFactory()
        book = BookFactory(authors=authors, publisher=publisher)

        assert book.title is not None
        assert book.publisher == publisher
        assert book.authors.count() == len(authors)

    def test_book_title_min_length_validation(self):
        book = BookFactory.build(title="It")
        with pytest.raises(ValidationError) as excinfo:
            book.full_clean()  # This will call the clean() method of the model
        assert "Book title must be at least 5 characters long." in str(excinfo.value)
