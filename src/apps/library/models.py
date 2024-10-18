from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel


class Author(TimeStampedModel):
    name = models.CharField(_("name"), max_length=100)
    bio = models.TextField(_("biography"))

    def __str__(self):
        return self.name

    def clean(self):
        valid_name_min_length = 3
        if len(self.name) < valid_name_min_length:
            msg = _("Author name must be at least 3 characters long.")
            raise ValidationError(msg)

    class Meta:
        ordering = ["id"]


class Publisher(TimeStampedModel):
    name = models.CharField(_("name"), max_length=100)
    website = models.URLField(_("website"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["id"]


class Book(TimeStampedModel):
    STATUS_CHOICES = Choices(
        ("draft", _("Draft")),
        ("published", _("Published")),
    )

    title = models.CharField(_("title"), max_length=200)
    description = models.TextField(_("description"))
    authors = models.ManyToManyField(
        Author,
        verbose_name=_("authors"),
        related_name="books",
    )
    publisher = models.ForeignKey(
        Publisher,
        verbose_name=_("publisher"),
        related_name="books",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        _("status"),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.draft,
        max_length=20,
    )

    def __str__(self):
        return self.title

    def clean(self):
        valid_title_min_length = 5
        if len(self.title) < valid_title_min_length:
            msg = _("Book title must be at least 5 characters long.")
            raise ValidationError(msg)

    class Meta:
        ordering = ["id"]
