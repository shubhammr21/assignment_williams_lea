import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LibraryConfig(AppConfig):
    name = "src.apps.library"
    verbose_name = _("Library")

    def ready(self):
        with contextlib.suppress(ImportError):
            import src.apps.library.signals  # noqa: F401
