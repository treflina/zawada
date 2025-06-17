from datetime import date
from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.validators import RegexValidator
from django.db import models
from PIL import Image as PILImage, ImageOps

from wagtail.admin.panels import FieldPanel
from wagtail.documents.models import AbstractDocument, Document
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.models import LockableMixin, Collection
from wagtail.snippets.models import register_snippet

from .utils import convert_bytes, extract_extension


class CustomDocument(AbstractDocument):
    @property
    def get_extension(self):
        return extract_extension(self.file)

    @property
    def get_size(self):
        return convert_bytes(self.file_size)

    admin_form_fields = Document.admin_form_fields


class CustomImage(AbstractImage):

    priority = models.BooleanField(
        default=False,
        verbose_name="wyróżnienie zdjęcia",
        help_text="Zdjęcie wyróżnione wyświetla się jako zdjęcie główne galerii.",
    )
    admin_form_fields = Image.admin_form_fields + (
        "priority",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if (
            self.width > 1200 or self.height > 1200
        ) and self.collection.name != "Zdjęcia - rozmiar oryginalny":
            img = PILImage.open(self.file.path)
            img = ImageOps.exif_transpose(img)
            img.thumbnail((1200, 1200))
            width, height = img.size
            img.save(self.file.path)
            img.close()

            if self.width != width or self.height != height:
                self.width = width
                self.height = height
                self.file_size = self.file.size
                self.save(update_fields=["width", "height", "file_size"])


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        CustomImage, on_delete=models.CASCADE, related_name="renditions"
    )

    class Meta:
        unique_together = (("image", "filter_spec", "focal_point_key"),)


class PagePaginationMixin:
    """Mixin that handles pagination for index pages giving an ability to use page
    range in case of too many subpages"""

    def pagination(self, request, posts, num=12):
        paginator = Paginator(posts, num)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        index = posts.number - 1
        max_index = len(paginator.page_range)
        start_index = index - 2 if index >= 2 else 0
        end_index = index + 2 if index <= max_index - 2 else max_index
        page_range = paginator.page_range[start_index:end_index]
        return posts, page_range

    class Meta:
        abstract = True


class SchoolYearSnippet(LockableMixin, models.Model):
    """School year for a snippet."""

    year_name_validator = RegexValidator(
        regex=r'^\d{4}/\d{4}$',
        message="Pole musi mieć format 'YYYY/YYYY', np. '2023/2024'."
    )

    name = models.CharField(
        max_length=9,
        verbose_name="rok szkolny",
        unique=True,
        validators=[year_name_validator],)

    years_widget = forms.TextInput(
        attrs = {
            'placeholder': 'YYYY/YYYY'
        }
    )

    panels = [
        FieldPanel("name",
        widget=years_widget,
        help_text="""Po zapisaniu nowego roku szkolnego,
    automatycznie zostanie utworzona kolekcja 'Galerie - <rok szkolny>'."""),
    ]

    @property
    def urlname(self):
        urlencodedname = self.name.replace("/", "")
        return urlencodedname

    class Meta:
        verbose_name = "Rok szkolny"
        verbose_name_plural = "Rok szkolny"
        ordering = ["-name",]


    def __str__(self):
        return self.name


class EventSnippet(models.Model):
    date = models.DateField(verbose_name="Data")
    description = models.TextField(verbose_name="Opis wydarzenia")

    panels = [
        FieldPanel("date"),
        FieldPanel("description"),
    ]

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"

    def __str__(self):
        return f"{self.date}: {self.description}"

    @property
    def is_past(self):
        return date.today() > self.date
