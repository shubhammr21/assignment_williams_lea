# tests/factories.py
from factory import Faker
from factory import SubFactory
from factory import post_generation
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from ..models import Author
from ..models import Book
from ..models import Publisher


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = Author

    name = Faker("name")
    bio = Faker("text")


class PublisherFactory(DjangoModelFactory):
    class Meta:
        model = Publisher

    name = Faker("company")
    website = Faker("url")


class BookFactory(DjangoModelFactory):
    class Meta:
        model = Book
        skip_postgeneration_save = True

    title = Faker("sentence", nb_words=4)
    description = Faker("paragraph")
    publisher = SubFactory(PublisherFactory)
    status = FuzzyChoice(["draft", "published"])

    @post_generation
    def authors(self, create, extracted, **kwargs):
        if create and extracted:
            for author in extracted:
                self.authors.add(author)
        if create:
            self.save()
