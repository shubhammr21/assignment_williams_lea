import pytest

from src.apps.library.tests.factories import AuthorFactory

from ..repositories import AuthorRepository


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
