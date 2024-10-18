from .models import Author
from .models import Book
from .models import Publisher


class AuthorRepository:
    @staticmethod
    def get_all():
        return Author.objects.all()

    @staticmethod
    def get_by_id(author_id):
        return Author.objects.get(id=author_id)


class PublisherRepository:
    @staticmethod
    def get_all():
        return Publisher.objects.all()

    @staticmethod
    def get_by_id(publish_id):
        return Publisher.objects.get(id=publish_id)


class BookRepository:
    @staticmethod
    def get_all():
        return Book.objects.all()

    @staticmethod
    def get_by_status(status):
        return Book.objects.filter(status=status)

    @staticmethod
    def get_by_id(book_id):
        return Book.objects.get(id=book_id)
