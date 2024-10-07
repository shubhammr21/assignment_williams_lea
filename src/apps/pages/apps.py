import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "src.apps.pages"
    verbose_name = _("pages")

    def ready(self):
        with contextlib.suppress(ImportError):
            import src.apps.pages.signals  # noqa: F401
