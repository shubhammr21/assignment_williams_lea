from .repositories import AuthorRepository
from .repositories import PublisherRepository


class AuthorService:
    @staticmethod
    def list_authors():
        return AuthorRepository.get_all()

    @staticmethod
    def get_author_by_id(author_id):
        return AuthorRepository.get_by_id(author_id)


class PublisherService:
    @staticmethod
    def list_publishers():
        return PublisherRepository.get_all()

    @staticmethod
    def get_publisher_by_id(publisher_id):
        return PublisherRepository.get_by_id(publisher_id)
