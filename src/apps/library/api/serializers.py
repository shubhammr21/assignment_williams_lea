from rest_framework import serializers

from ..models import Author
from ..models import Book
from ..models import Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name", "bio"]


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["id", "name", "website"]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        source="authors",
        write_only=True,
    )
    publisher = PublisherSerializer(read_only=True)
    publisher_id = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
        source="publisher",
        write_only=True,
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "description",
            "authors",
            "author_ids",
            "publisher",
            "publisher_id",
            "status",
        ]
