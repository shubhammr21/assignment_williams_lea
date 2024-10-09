from django.utils.translation import gettext_lazy as _

from src.exceptions.base import BaseError


class XMLFetchError(BaseError):
    """Custom exception to handle XML fetching errors."""

    default_detail = _("Unable to fetch XML")
