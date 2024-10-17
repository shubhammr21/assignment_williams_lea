# services.py
from .repositories import AuthorRepository


class AuthorService:
    @staticmethod
    def list_authors():
        return AuthorRepository.get_all()

    @staticmethod
    def get_author_by_id(author_id):
        return AuthorRepository.get_by_id(author_id)
