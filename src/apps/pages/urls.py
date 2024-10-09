from django.urls import path
from django.views.generic import TemplateView

from .views import transform_xml
from .views import transform_xml_2

app_name = "pages"

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("transform/", transform_xml, name="transform_xml"),
    path("transform2/", transform_xml_2, name="transform_xml"),
]
