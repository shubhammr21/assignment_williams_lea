from django.shortcuts import render
from django.views import View

from .context_processors.legislation_context import LegislationContext
from .fetchers.xml_fetcher import XMLFetcher
from .transformers.xslt_transformer import XSLTTransformer

XML_URL = "https://www.legislation.gov.uk/uksi/2024/979/contents/made/data.xml"


class LegislationWithXSLTView(View):
    def get(self, request, *args, **kwargs):
        # Fetch XML content
        xml_content = XMLFetcher.fetch(XML_URL)
        xslt_content = XSLTTransformer.get_xslt_content(
            "pages/xslt/legislation.xslt",
        )
        html_content = XSLTTransformer.transform(xml_content, xslt_content)
        return render(
            request,
            "pages/transform.html",
            {"html_content": html_content},
        )


legislation_with_xslt_view = LegislationWithXSLTView.as_view()


class LegislationWithXMLParserView(View):
    def get(self, request, *args, **kwargs):
        # Fetch XML content
        xml_content = XMLFetcher.fetch(XML_URL)
        context = LegislationContext().get_context(xml_content)
        return render(request, "pages/transform2.html", context)


legislation_with_xml_parser_view = LegislationWithXMLParserView.as_view()
