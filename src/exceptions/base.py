from http import HTTPStatus

from django.utils.translation import gettext_lazy as _


class BaseError(Exception):
    """
    Base class for exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """

    default_detail = _("A server error occurred.")
    default_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, detail=None, code=None):
        self.detail = detail or self.default_detail
        self.code = code or self.default_code

    def __str__(self):
        return str(self.detail)
