from django.test import TestCase

from ..context_processors.legislation_context import LegislationContext


class LegislationContextTests(TestCase):
    def test_get_context_success(self):
        xml_content = b"""
        <root
            xmlns:leg="http://www.legislation.gov.uk/namespaces/legislation"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:atom="http://www.w3.org/2005/Atom">
            <dc:title>Sample Legislation</dc:title>
            <leg:SecondaryPrelims DocumentURI="http://example.com/doc">
                <leg:Number>1</leg:Number>
                <leg:Title>Title</leg:Title>
                <leg:Subject>
                    <leg:Title>Subject Title</leg:Title>
                </leg:Subject>
                <leg:MadeDate>
                    <leg:Text>Made Date Text</leg:Text>
                    <leg:DateText>2024-10-09</leg:DateText>
                </leg:MadeDate>
                <leg:ComingIntoForce>
                    <leg:Text>Coming Into Force Text</leg:Text>
                    <leg:DateText>2024-10-10</leg:DateText>
                </leg:ComingIntoForce>
            </leg:SecondaryPrelims>
            <atom:link title="signature" href="http://example.com/signature" />
            <atom:link title="note" href="http://example.com/note" />
        </root>
        """

        context = LegislationContext().get_context(xml_content)

        assert context["table_of_contents"]["title"] == "Sample Legislation"
        assert (
            context["table_of_contents"]["secondary_prelims_document_uri"]
            == "http://example.com/doc"
        )
        assert context["content"]["title"] == "Title"
        assert context["content"]["made_date"] == "2024-10-09"

    def test_get_context_no_secondary_prelims(self):
        xml_content = b"""
        <root
            xmlns:leg="http://www.legislation.gov.uk/namespaces/legislation"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:atom="http://www.w3.org/2005/Atom">
            <dc:title>Sample Legislation</dc:title>
            <atom:link title="signature" href="http://example.com/signature" />
            <atom:link title="note" href="http://example.com/note" />
        </root>
        """

        context = LegislationContext().get_context(xml_content)

        assert context["table_of_contents"]["title"] == "Sample Legislation"
        assert context["table_of_contents"]["secondary_prelims_document_uri"] == "#"
        assert context["content"] == {}
