from http import HTTPStatus
from unittest.mock import patch

import pytest
from django.contrib import messages
from django.template import Context
from django.template import Template
from django.template.response import TemplateResponse
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from src.apps.pages.exceptions import XMLFetchError


class TestTemplatesRendering:
    @pytest.mark.django_db
    def test_home_page_rendered_in_view(self):
        """
        Test if the base template is correctly rendered in a view that extends it.
        """
        client = Client()

        response = client.get(reverse("pages:home"))

        assert response.status_code == HTTPStatus.OK

        assert b"<main" in response.content
        assert b"Welcome to the Assignment Overview" in response.content
        assert b"<footer" in response.content
        assert b"My Awesome Project. All rights reserved." in response.content

    def test_empty_template_extends_base(self):
        """
        Test that an empty template extends base.html without overriding any blocks.
        """

        template = Template('{% extends "base.html" %}')

        context = Context({})
        rendered_template = template.render(context)
        assert '<link rel="stylesheet" href="/static' in rendered_template
        assert "<nav " in rendered_template
        assert "Home" in rendered_template
        assert "With XSLT" in rendered_template
        assert "With Parsing XML" in rendered_template
        assert "<header " in rendered_template
        assert "legislation" in rendered_template
        assert "<main" in rendered_template
        assert "<h2>Main Content Area</h2>" in rendered_template
        assert "<aside " in rendered_template
        assert "<h3>Sidebar</h3>" in rendered_template
        assert "<footer" in rendered_template
        assert "My Awesome Project. All rights reserved." in rendered_template

    @pytest.mark.django_db
    def test_messages_block_rendered_in_base_template(self):
        client = Client()

        response = client.get(reverse("pages:home"))
        messages.success(response.wsgi_request, "Test message.")
        messages.info(response.wsgi_request, "This is a test info message..")
        messages.error(response.wsgi_request, "This is a test error message.")

        template_name = "pages/home.html"
        all_messages = messages.get_messages(response.wsgi_request)
        context = {
            "messages": all_messages,
        }

        template = TemplateResponse(response.wsgi_request, template_name, context)

        rendered_content = template.render().content
        assert len(all_messages) == 3
        assert b"Test message." in rendered_content

        assert b"alert-info" in rendered_content
        assert b"This is a test info message." in rendered_content

        assert b"alert-error" in rendered_content
        assert b"This is a test error message." in rendered_content

        assert b"btn-close" in rendered_content


class LegislationViewTests(TestCase):
    @patch("src.apps.pages.fetchers.xml_fetcher.XMLFetcher.fetch")
    @patch("src.apps.pages.transformers.xslt_transformer.XSLTTransformer.transform")
    def test_transform_view_success(self, mock_transform, mock_fetch):
        mock_fetch.return_value = b"<root><element>data</element></root>"
        mock_transform.return_value = "<h1>data</h1>"

        response = self.client.get(reverse("pages:transform_xml"))

        assert response.status_code == HTTPStatus.OK
        self.assertContains(response, "<h1>data</h1>")

    @patch("src.apps.pages.fetchers.xml_fetcher.XMLFetcher.fetch")
    def test_transform_view_fetch_failure(self, mock_fetch):
        mock_fetch.side_effect = XMLFetchError("Fetch failed")
        response = self.client.get(reverse("pages:transform_xml"))
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    @patch("src.apps.pages.fetchers.xml_fetcher.XMLFetcher.fetch")
    @patch(
        "src.apps.pages.context_processors.legislation_context.LegislationContext.get_context",
    )
    def test_transform_view_context_success(self, mock_get_context, mock_fetch):
        mock_fetch.return_value = b"<root><element>data</element></root>"
        mock_get_context.return_value = {
            "table_of_contents": {
                "title": "Title",
                "secondary_prelims_document_uri": "http://example.com/introduction/made",
                "contents": [
                    {
                        "document_uri": "http://example.com/article/1/made",
                        "contents_number": "1",
                        "contents_title": "item 1",
                    },
                    {
                        "document_uri": "http://example.com/article/2/made",
                        "contents_number": "2",
                        "contents_title": "item 2",
                    },
                ],
                "signature_link_href": "http://example.com/signature/made",
                "note_link_href": "http://example.com/note/made",
            },
            "content": {
                "number": "2024 No. 979",
                "title": "Content Title",
                "subject": "Education, England",
                "made_date_text": "Made",
                "made_date": "25th September 2024",
                "coming_into_force_text": "Coming into force",
                "coming_into_force_date": "1st October 2024",
                "introductory_text": "Introduction test",
                "enacting_text": "Enacting Text",
            },
        }

        response = self.client.get(reverse("pages:transform_xml_2"))

        assert response.status_code == HTTPStatus.OK
        self.assertContains(response, "Title")
