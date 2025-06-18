from django.db import models
from django.utils.timezone import now
from wagtail.admin.panels import (
    FieldPanel
)
from wagtail.fields import StreamField
from wagtail.models import Page

from core.blocks import BaseStreamBlock


class NewsIndexPage(Page):

    template = "news/news_index_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["news.NewsPage"]

    content_panels = Page.content_panels

    class Meta:
        verbose_name = "Lista aktualności"


class NewsPage(Page):

    template = "news/news_page.html"
    parent_page_types = ["news.NewsIndexPage"]
    subpage_types = []

    publish_date = models.DateField(
        blank=True,
        null=True,
        default=now,
        verbose_name="Data publikacji",
        help_text="""Data publikacji wyświetlana na stronie.""",
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Treść", blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("publish_date"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Aktualności"



