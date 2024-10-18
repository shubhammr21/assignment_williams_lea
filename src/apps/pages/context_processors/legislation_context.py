import lxml.etree as ET


class LegislationContext:
    def get_context(self, xml_content: bytes | str) -> dict:
        """Parse XML content and extract relevant legislation data."""
        root = ET.fromstring(xml_content)
        ns = {
            "leg": "http://www.legislation.gov.uk/namespaces/legislation",
            "dc": "http://purl.org/dc/elements/1.1/",
            "atom": "http://www.w3.org/2005/Atom",
            "ukm": "http://www.legislation.gov.uk/namespaces/metadata",
            "xsl": "http://www.w3.org/1999/XSL/Transform",
        }

        title = self.get_text(root.find(".//dc:title", ns))
        secondary_prelims = root.find(".//leg:SecondaryPrelims", ns)
        secondary_prelims_uri = self.get_attrib(secondary_prelims, "DocumentURI", "#")
        contents = self.extract_contents(root, ns)
        secondary_data = self.extract_secondary_data(secondary_prelims, ns)

        signature_link_href = root.find('.//atom:link[@title="signature"]', ns).get(
            "href",
        )
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

    def extract_contents(self, root, ns):
        """Extract contents from XML."""
        contents = []
        for contents_item in root.findall(".//leg:ContentsItem", ns):
            item = {
                "document_uri": contents_item.get("DocumentURI"),
                "contents_number": self.get_text(
                    contents_item.find("leg:ContentsNumber", ns),
                ),
                "contents_title": self.get_text(
                    contents_item.find("leg:ContentsTitle", ns),
                ),
            }
            contents.append(item)
        return contents

    def extract_secondary_data(self, secondary_prelims, ns):
        """Extract secondary prelims data from XML."""
        return {
            "number": secondary_prelims.find("leg:Number", ns).text.strip(),
            "title": secondary_prelims.find("leg:Title", ns).text.strip(),
            "subject": self.get_text(
                secondary_prelims.find(".//leg:Subject/leg:Title", ns),
            ),
            "made_date_text": self.get_text(
                secondary_prelims.find(".//leg:MadeDate/leg:Text", ns),
            ),
            "made_date": self.get_text(
                secondary_prelims.find(".//leg:MadeDate/leg:DateText", ns),
            ),
            "coming_into_force_text": self.get_text(
                secondary_prelims.find(".//leg:ComingIntoForce/leg:Text", ns),
            ),
            "coming_into_force_date": self.get_text(
                secondary_prelims.find(".//leg:ComingIntoForce/leg:DateText", ns),
            ),
            "introductory_text": self.get_text(
                secondary_prelims.find(".//leg:IntroductoryText/leg:P/leg:Text", ns),
            ),
            "enacting_text": self.get_text(
                secondary_prelims.find(".//leg:EnactingText/leg:Para/leg:Text", ns),
            ),
        }

    @staticmethod
    def get_text(el, default=None):
        """Get text from an XML element."""
        if el is None:
            return default
        return el.text.strip()

    @staticmethod
    def get_attrib(el, attrib, default=None):
        """Get attrib from an XML element."""
        if el is None:
            return default
        return el.get(attrib, default)
