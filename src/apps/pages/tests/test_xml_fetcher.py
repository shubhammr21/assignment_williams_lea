from unittest.mock import Mock
from unittest.mock import patch

import pytest
import requests
from django.test import TestCase

from ..exceptions import XMLFetchError
from ..fetchers.xml_fetcher import XMLFetcher


class XMLFetcherTests(TestCase):
    @patch("src.apps.pages.fetchers.xml_fetcher.requests.get")
    def test_fetch_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<root><element>data</element></root>"
        mock_get.return_value = mock_response

        result = XMLFetcher.fetch("http://example.com")

        assert result == b"<root><element>data</element></root>"
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("src.apps.pages.fetchers.xml_fetcher.requests.get")
    def test_fetch_failure(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "404 Client Error: Not Found for url: http://example.com",
        )
        mock_get.return_value = mock_response

        with pytest.raises(XMLFetchError):
            XMLFetcher.fetch("http://example.com")
