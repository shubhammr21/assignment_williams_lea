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


def transform_xml_2(request):
    # Load the XML and XSLT files
    resp = requests.get(
        "https://www.legislation.gov.uk/uksi/2024/979/contents/made/data.xml",
    )
    if resp.status_code != 200:
        return render(request, "500.html", status=500)
    context = get_legislation_context(resp.content)

    return render(request, "pages/transform2.html", context)


def get_legislation_context(xml_content: bytes | str):
    # Load and parse the XML file
    # Parse the XML
    root = ET.fromstring(xml_content)

    # Extract relevant data using XPath with namespace support
    ns = {
        "leg": "http://www.legislation.gov.uk/namespaces/legislation",
        "dc": "http://purl.org/dc/elements/1.1/",
        "atom": "http://www.w3.org/2005/Atom",
        "ukm": "http://www.legislation.gov.uk/namespaces/metadata",
        "xsl": "http://www.w3.org/1999/XSL/Transform",
    }

    title = root.find(".//dc:title", ns).text.strip()

    secondary_prelims = root.find(".//leg:SecondaryPrelims", ns)
    secondary_prelims_uri = secondary_prelims.get("DocumentURI") or "#"

    contents = []
    for contents_item in root.findall(".//leg:ContentsItem", ns):
        item = {
            "document_uri": contents_item.get("DocumentURI"),
            "contents_number": contents_item.find(
                "leg:ContentsNumber",
                ns,
            ).text.strip(),
            "contents_title": contents_item.find("leg:ContentsTitle", ns).text.strip(),
        }
        contents.append(item)

    secondary_data = {}
    if secondary_prelims is not None:
        secondary_data = {
            "number": secondary_prelims.find("leg:Number", ns).text.strip(),
            "title": secondary_prelims.find("leg:Title", ns).text.strip(),
            "subject": secondary_prelims.find(
                ".//leg:Subject/leg:Title",
                ns,
            ).text.strip(),
            "made_date_text": secondary_prelims.find(
                ".//leg:MadeDate/leg:Text",
                ns,
            ).text.strip(),
            "made_date": secondary_prelims.find(
                ".//leg:MadeDate/leg:DateText",
                ns,
            ).text.strip(),
            "coming_into_force_text": secondary_prelims.find(
                ".//leg:ComingIntoForce/leg:Text",
                ns,
            ).text.strip(),
            "coming_into_force_date": secondary_prelims.find(
                ".//leg:ComingIntoForce/leg:DateText",
                ns,
            ).text.strip(),
            "introductory_text": secondary_prelims.find(
                ".//leg:IntroductoryText/leg:P/leg:Text",
                ns,
            ).text.strip(),
            "enacting_text": secondary_prelims.find(
                ".//leg:EnactingText/leg:Para/leg:Text",
                ns,
            ).text.strip(),
        }

    signature_link_href = root.find('.//atom:link[@title="signature"]', ns).get("href")
    note_link_href = root.find('.//atom:link[@title="note"]', ns).get("href")

    return {
        "table_of_contents": {
            "title": title,
            "secondary_prelims_document_uri": secondary_prelims_uri,
            "contents": contents,
            "signature_link_href": signature_link_href,
            "note_link_href": note_link_href,
        },
        "content": secondary_data,
    }
