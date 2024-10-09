import lxml.etree as ET
import pytest
from django.template.loader import render_to_string
from django.test import TestCase

from ..transformers.xslt_transformer import XSLTTransformer


class XSLTTransformerTests(TestCase):
    def test_transform_success(self):
        xml_content = b"<root><element>data</element></root>"
        xslt_content = b"""
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:template match="/">
                <html><body><h1><xsl:value-of select="root/element"/></h1></body></html>
            </xsl:template>
        </xsl:stylesheet>
        """

        result = XSLTTransformer.transform(xml_content, xslt_content)

        assert "<h1>data</h1>" in result

    def test_get_xslt_content_success(self):
        xslt_content = render_to_string("pages/xslt/legislation.xslt").encode("utf-8")

        result = XSLTTransformer.get_xslt_content("pages/xslt/legislation.xslt")

        assert result == xslt_content

    def test_transform_invalid_xml(self):
        invalid_xml_content = b"<root><element>data</root>"  # Invalid XML
        xslt_content = b"""
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
            <xsl:template match="/">
                <html><body><h1><xsl:value-of select="root/element"/></h1></body></html>
            </xsl:template>
        </xsl:stylesheet>
        """

        with pytest.raises(ET.XMLSyntaxError):
            XSLTTransformer.transform(invalid_xml_content, xslt_content)
