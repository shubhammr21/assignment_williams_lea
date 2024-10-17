# repositories.py
from .models import Author


class AuthorRepository:
    @staticmethod
    def get_all():
        return Author.objects.all()

    @staticmethod
    def get_by_id(author_id):
        return Author.objects.get(id=author_id)
