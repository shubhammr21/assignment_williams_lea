from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command

from ..models import Author
from ..models import Book
from ..models import Publisher


@pytest.mark.django_db
class TestDataGenerationCommand:
    @pytest.fixture
    def mock_tqdm(self):  # noqa: PT004
        # Mock tqdm to disable progress bar output during tests
        with patch("tqdm.tqdm", side_effect=lambda x, **kwargs: x):
            yield

    def test_command_creates_publishers(self, mock_tqdm):
        # Run the command with a small count
        count = 10
        batch = 5
        out = StringIO()
        call_command(
            "generate_random_library_data",
            "--count",
            f"{count}",
            "--batch",
            f"{batch}",
            stdout=out,
        )

        # Check that the expected number of publishers were created
        assert Publisher.objects.count() == count
        assert Author.objects.count() == count
        assert Book.objects.count() == count

    def test_command_with_different_batch_size(self, mock_tqdm):
        # Run the command with a larger batch size than the total count
        count = 10
        batch = 15
        out = StringIO()
        call_command(
            "generate_random_library_data",
            "--count",
            f"{count}",
            "--batch",
            f"{batch}",
            stdout=out,
        )

        # Ensure objects were created
        assert Publisher.objects.count() == count
        assert Author.objects.count() == count
        assert Book.objects.count() == count

    def test_command_outputs_progress_messages(self, mock_tqdm):
        # Capture stdout to check output messages
        out = StringIO()
        call_command(
            "generate_random_library_data",
            "--count",
            "10",
            "--batch",
            "5",
            stdout=out,
        )

        output = out.getvalue()

        # Check if output contains expected messages
        assert "Inserting 10 records in batches of 5..." in output
        assert "Inserted 10 publishers" in output
        assert "Inserted 10 authors" in output
        assert "Inserted 10 books and assigned authors" in output
        assert "Total time taken" in output
        assert "Records per second" in output

    @patch("django.db.transaction.atomic")
    def test_transaction_is_used(self, mock_atomic, mock_tqdm):
        # Run the command and check that transaction.atomic is used
        call_command(
            "generate_random_library_data",
            "--count",
            "10",
            "--batch",
            "5",
        )

        # Ensure that a transaction was started
        assert mock_atomic.call_count > 0
