from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from src.apps.pages.exceptions import XMLFetchError


class LegislationViewTests(TestCase):
    @patch("src.apps.pages.fetchers.xml_fetcher.XMLFetcher.fetch")
    @patch("src.apps.pages.transformers.xslt_transformer.XSLTTransformer.transform")
    def test_transform_view_success(self, mock_transform, mock_fetch):
        mock_fetch.return_value = b"<root><element>data</element></root>"
        mock_transform.return_value = "<h1>data</h1>"

        response = self.client.get(reverse("pages:transform_xml"))

        assert response.status_code == 200
        self.assertContains(response, "<h1>data</h1>")

    @patch("src.apps.pages.fetchers.xml_fetcher.XMLFetcher.fetch")
    def test_transform_view_fetch_failure(self, mock_fetch):
        mock_fetch.side_effect = XMLFetchError("Fetch failed")
        response = self.client.get(reverse("pages:transform_xml"))
        assert response.status_code == 500

    @patch("src.apps.pages.fetchers.xml_fetcher.XMLFetcher.fetch")
    @patch(
        "src.apps.pages.context_processors.legislation_context.LegislationContext.get_context",
    )
    def test_transform_view_context_success(self, mock_get_context, mock_fetch):
        mock_fetch.return_value = b"<root><element>data</element></root>"
        mock_get_context.return_value = {
            "table_of_contents": {
                "title": "Title",
                "secondary_prelims_document_uri": "#",
            },
            "content": {},
        }

        response = self.client.get(reverse("pages:transform_xml_2"))

        assert response.status_code == 200
        self.assertContains(response, "Title")
