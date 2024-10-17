from http import HTTPStatus
from unittest.mock import MagicMock

import pytest
from django.http import HttpResponse
from django.test import RequestFactory

from src.exceptions.base import BaseError

from ..exception_handler import ExceptionHandlingMiddleware


@pytest.fixture
def get_response_mock():
    """A mock get_response function that will be passed to the middleware."""
    return MagicMock(return_value=HttpResponse("OK"))


@pytest.fixture
def middleware(get_response_mock):
    """Initialize the ExceptionHandlingMiddleware with the mocked get_response."""
    return ExceptionHandlingMiddleware(get_response=get_response_mock)


@pytest.fixture
def request_factory():
    """Provide a Django request factory to simulate HTTP requests."""
    return RequestFactory()


@pytest.mark.django_db
class TestExceptionHandlingMiddleware:
    def test_no_exception(self, middleware, request_factory, get_response_mock):
        """
        Test that the middleware does nothing when there is no exception.
        """

        request = request_factory.get("/")

        response = middleware(request)

        assert response.status_code == 200
        get_response_mock.assert_called_once_with(request)
        assert response.content == b"OK"

    def test_process_exception_with_base_error(self, middleware, request_factory):
        """
        Test that the middleware handles BaseError and returns the proper response.
        """

        class TestBaseError(BaseError):
            default_code = HTTPStatus.BAD_REQUEST
            default_detail = "Test error detail"

        request = request_factory.get("/")
        exception = TestBaseError()

        response = middleware.process_exception(request, exception)

        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert b"Test error detail" in response.content

    def test_process_exception_with_generic_unhandled_exception(
        self,
        middleware,
        request_factory,
    ):
        """
        Test that the middleware handles generic Exception and returns a 500 response.
        """

        request = request_factory.get("/")
        exception = Exception("Something went wrong")

        response = middleware.process_exception(request, exception)

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
