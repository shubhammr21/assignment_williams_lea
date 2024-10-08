import lxml.etree as ET
import requests
from django.shortcuts import render
from django.template.loader import render_to_string


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
    parser = ET.XMLParser(remove_blank_text=True, no_network=True)

    xml = ET.fromstring(xml_content, parser)  # noqa: S320
    xslt = ET.fromstring(xslt_content, parser)  # noqa: S320

    transform = ET.XSLT(xslt)
    result = transform(xml)

    return str(result)


def transform_xml(request):
    # Load the XML and XSLT files
    resp = requests.get(
        "https://www.legislation.gov.uk/uksi/2024/979/contents/made/data.xml",
    )
    if resp.status_code != 200:
        return render(request, "500.html", status=500)
    html_content = transform_xml_to_html_with_xslt(
        resp.content,
        render_to_string("pages/xslt/legislation.xslt").encode("utf-8"),
    )
    # Render the content in a template
    return render(request, "pages/transform.html", {"html_content": html_content})
