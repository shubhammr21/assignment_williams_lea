from django.urls import path
from django.views.generic import TemplateView

from .views import legislation_with_xml_parser_view
from .views import legislation_with_xslt_view

app_name = "pages"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("transform/", legislation_with_xslt_view, name="transform_xml"),
    path("transform2/", legislation_with_xml_parser_view, name="transform_xml_2"),
]
