import lxml.etree as ET
from django.conf import settings
from django.shortcuts import render


def transform_xml_to_html_with_xslt(
    xml_content: bytes | str,
    xslt_content: bytes | str,
) -> str:
    """
    Helper function to transform XML content using XSLT and return the
     resulting HTML as a string.

    Args:
    - xml_content (str): The XML content as a string.
    - xslt_content (str): The XSLT content as a string.

    Returns:
    - str: The transformed HTML string.
    """
    # Create a secure XML parser that disables external entities
    parser = ET.XMLParser(remove_blank_text=True, no_network=True)

    xml = ET.fromstring(xml_content, parser)  # noqa: S320
    xslt = ET.fromstring(xslt_content, parser)  # noqa: S320

    transform = ET.XSLT(xslt)
    result = transform(xml)

    return str(result)


def transform_xml(request):
    # Load the XML and XSLT files
    xml_file_path = settings.APPS_DIR / "static" / "pages" / "products.xml"
    xslt_file_path = settings.APPS_DIR / "static" / "pages" / "style.xslt"
    html_content = transform_xml_to_html_with_xslt(
        xml_file_path.read_bytes(),
        xslt_file_path.read_bytes(),
    )
    # Render the content in a template
    return render(request, "pages/transform.html", {"html_content": html_content})
