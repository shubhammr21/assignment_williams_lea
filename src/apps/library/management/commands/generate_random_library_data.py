import random
import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from faker import Faker
from tqdm import tqdm

from ...models import Author
from ...models import Book
from ...models import Publisher

# Initialize Faker
faker = Faker()


class Command(BaseCommand):
    help = (
        "Generate random data for Authors, Publishers, and Books with progress tracking"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            help="The number of data rows to create",
            default=1000,
        )
        parser.add_argument(
            "--batch",
            type=int,
            help="Define batch size to process",
            default=100,
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        count = kwargs["count"]
        batch_size = kwargs["batch"]

        total_start_time = time.time()

        self.stdout.write(
            self.style.SUCCESS(
                f"Inserting {count} records in batches of {batch_size}...",
            ),
        )

        # Insert publishers
        start_time = time.time()
        self._bulk_insert_publishers(count, batch_size)
        elapsed_time = time.time() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {count} publishers in {elapsed_time:.2f} seconds",
            ),
        )

        # Insert authors
        start_time = time.time()
        self._bulk_insert_authors(count, batch_size)
        elapsed_time = time.time() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {count} authors in {elapsed_time:.2f} seconds",
            ),
        )

        # Insert books with authors
        start_time = time.time()
        self._bulk_insert_books_with_authors(count, batch_size)
        elapsed_time = time.time() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Inserted {count} books and assigned authors in {elapsed_time:.2f} seconds",
            ),
        )

        # Display total time taken
        total_elapsed_time = time.time() - total_start_time
        self.stdout.write(
            self.style.SUCCESS(f"Total time taken: {total_elapsed_time:.2f} seconds"),
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Records per second: {count / total_elapsed_time:.2f} records/sec",
            ),
        )

    def _bulk_insert_publishers(self, count, batch_size):
        """Bulk insert publishers with progress tracking."""
        publishers = []
        for _ in tqdm(range(count), desc="Inserting Publishers", unit="publisher"):
            publishers.append(Publisher(name=faker.company(), website=faker.url()))

            if len(publishers) >= batch_size:
                Publisher.objects.bulk_create(publishers)
                publishers = []

        if publishers:
            Publisher.objects.bulk_create(publishers)

    def _bulk_insert_authors(self, count, batch_size):
        """Bulk insert authors with progress tracking."""
        authors = []
        for _ in tqdm(range(count), desc="Inserting Authors", unit="author"):
            authors.append(Author(name=faker.name(), bio=faker.text()))

            if len(authors) >= batch_size:
                Author.objects.bulk_create(authors)
                authors = []

        if authors:
            Author.objects.bulk_create(authors)

    def _bulk_insert_books_with_authors(self, count, batch_size):
        """Bulk insert books and assign authors with progress tracking."""
        books = []
        authors = list(Author.objects.all().values_list("id", flat=True))
        publishers = list(Publisher.objects.all().values_list("id", flat=True))
        book_author_relations = []

        for _ in tqdm(
            range(count),
            desc="Inserting Books and Assigning Authors",
            unit="book",
        ):
            # Pick a random publisher for each book
            publisher_id = random.choice(publishers)
            # book = Book(title=faker.catch_phrase(), description=faker.text(), author_id=random.choice(authors))
            book = Book(
                title=faker.catch_phrase(),
                description=faker.text(),
                publisher_id=publisher_id,
            )
            books.append(book)

            # Pick 1-3 random authors for each book
            random_author_ids = random.sample(authors, random.randint(1, 3))
            book_author_relations.append((book, random_author_ids))

            if len(books) >= batch_size:
                self._bulk_insert_books_and_authors(books, book_author_relations)
                books.clear()
                book_author_relations.clear()

        if books:
            self._bulk_insert_books_and_authors(books, book_author_relations)

    def _bulk_insert_books_and_authors(self, books, book_author_relations):
        """Bulk insert books and their many-to-many relationships."""
        Book.objects.bulk_create(books)

        # Prepare M2M relations for books and authors
        book_author_m2m_insert_data = []
        for book, author_ids in book_author_relations:
            # Use the latest book object to get its ID
            for author_id in author_ids:
                book_author_m2m_insert_data.append((book.id, author_id))

        # Prepare raw SQL to insert into the many-to-many relationship table
        if book_author_m2m_insert_data:
            with connection.cursor() as cursor:
                cursor.executemany(
                    "INSERT INTO library_book_authors (book_id, author_id) VALUES (%s, %s)",
                    book_author_m2m_insert_data,
                )
