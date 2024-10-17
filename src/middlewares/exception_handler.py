from http import HTTPStatus
from logging import getLogger

from django.shortcuts import render

from src.exceptions.base import BaseError

logger = getLogger()


class ExceptionHandlingMiddleware:
    """Handle uncaught exceptions instead of raising a 500."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, BaseError):
            logger.error(exception)
            return render(
                request,
                f"{exception.code}.html",
                {"exception": exception.detail},
                status=exception.code,
            )
        if isinstance(exception, Exception):  # noqa: RET503
            logger.exception(exception)
            return render(
                request,
                "500.html",
                {"error": str(exception)},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
