from django import forms
from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from wagtail.admin.panels import (
    FieldPanel,
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, path
from wagtail.fields import RichTextField
from wagtail.models import Collection, Page

from core.models import CustomImage, PagePaginationMixin, SchoolYearSnippet


class CustomSelect(forms.Select):
    """Allow for visual representation of 'depth' of collection in select"""

    def create_option(self, name, value, *args, **kwargs):
        option_dict = super().create_option(name, value, *args, **kwargs)
        instance = getattr(value, 'instance', None)
        if instance:
            option_dict['label'] = instance.get_indented_name()
        return option_dict


class GalleriesIndexPage(PagePaginationMixin, RoutablePageMixin, Page):
    template = "galleries/gallery_index_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["galleries.GalleryPage"]

    year = models.OneToOneField(
        "core.SchoolYearSnippet",
        blank=False,
        null=True,
        verbose_name="Rok szkolny",
        on_delete=models.PROTECT,
        related_name="+",
    )

    def clean(self):
        super().clean()
        new_title = f"Galerie zdjęć - {self.year.name}"
        self.title = new_title
        self.slug = f"galerie{slugify(self.year.name)}"

    def get_previous_index_page(self):
        return GalleriesIndexPage.objects.filter(
            year__name__gt=self.year.name
        ).order_by('year__name').first()

    def get_next_index_page(self):
        return GalleriesIndexPage.objects.filter(
            year__name__lt=self.year.name
        ).order_by('-year__name').first()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["years"] = SchoolYearSnippet.objects.all()
        galleries = GalleryPage.objects.specific().live() \
            .child_of(self).order_by("-publish_date", "-first_published_at")
        context["galleries"] = galleries
        context["prev_index"] = self.get_previous_index_page()
        context["next_index"] = self.get_next_index_page()
        context["gallery_page"] = "active"
        return context

    content_panels = [FieldPanel("year"),]
    search_fields = Page.search_fields

    class Meta:
        verbose_name = "Lista galerii zdjęć w roku szkolnym"


class GalleryPage(PagePaginationMixin, Page):
    """Gallery page that contains images and description of the gallery."""

    template = "galleries/gallery_detail_page.html"
    subpage_types = []
    parent_page_types = ["galleries.GalleriesIndexPage"]

    description = RichTextField(
        blank=True, null=True, verbose_name="Opis galerii", features=[]
    )

    publish_date = models.DateField(
        blank=True,
        null=True,
        default=now,
        verbose_name="Data publikacji",
        help_text="""Data publikacji wyświetlana na stronie.""",
    )

    collection = models.ForeignKey(
        Collection,
        limit_choices_to=~models.Q(name__in=['Root']), # do not allow 'root' selection
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='Wybierz kolekcję zdjęć do opublikowania.'
    )

    content_panels = Page.content_panels + [
        FieldPanel("publish_date"),
        FieldPanel("description"),
        FieldPanel('collection', widget=CustomSelect),
    ]

    def gallery_images(self):
        return CustomImage.objects.filter(collection=self.collection)

    @property
    def banner_image(self):
        images = self.gallery_images()
        return images.filter(priority=True).last() or images.last()

    def get_gallery_siblings(self):
        parent = self.get_parent()
        siblings = parent.get_children().specific().live()

        try:
            index = list(siblings).index(self)
        except ValueError:
            return None, None

        prev_gallery = siblings[index - 1] if index > 0 else None
        try:
            next_gallery = siblings[index + 1]
        except IndexError:
            next_gallery = None

        return prev_gallery, next_gallery

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["images"] = self.gallery_images()
        prev_gallery, next_gallery = self.get_gallery_siblings()
        context["next_gallery"] = prev_gallery
        context["prev_gallery"] = next_gallery
        context["gallery_page"] = "active"
        return context

    class Meta:
        verbose_name = "Galeria zdjęć"
        verbose_name_plural = "Galerie zdjęć"
