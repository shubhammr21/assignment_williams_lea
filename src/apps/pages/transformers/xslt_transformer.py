import lxml.etree as ET
from django.template.loader import render_to_string


class XSLTTransformer:
    @staticmethod
    def transform(xml_content: bytes | str, xslt_content: bytes | str) -> str:
        """Transform XML content using XSLT and return the resulting
        HTML as a string."""
        parser = ET.XMLParser(resolve_entities=False, no_network=True)
        xml = ET.fromstring(xml_content, parser)
        xslt = ET.fromstring(xslt_content, parser)
        transform = ET.XSLT(xslt)
        result = transform(xml)
        return str(result)

    @staticmethod
    def get_xslt_content(template_name: str) -> bytes:
        """Load XSLT content from a template."""
        return render_to_string(template_name).encode("utf-8")
