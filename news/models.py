from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from wagtail.admin.panels import (
    FieldPanel
)
from wagtail.fields import StreamField
from wagtail.models import Page

from core.blocks import BaseStreamBlock, BaseStreamWithFlagBlock
from core.models import PagePaginationMixin


class NewsIndexPage(PagePaginationMixin, Page):

    template = "news/news_index_page.html"
    parent_page_types = ["home.HomePage"]
    subpage_types = ["news.NewsPage", "news.NewsPage2"]

    content_panels = Page.content_panels

    class Meta:
        verbose_name = "Lista aktualności"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["news_page"] = "active"
        newspages = NewsPage2.objects.live().public().specific() \
                        .order_by("-publish_date", "-id")
        context["posts"], context["page_range"] = self.pagination(request, newspages, num=1)
        return context


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


class NewsPage2(Page):

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
        BaseStreamWithFlagBlock(), verbose_name="Treść", blank=True, use_json_field=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("publish_date"),
        FieldPanel("body"),
    ]

    class Meta:
        verbose_name = "Aktualności2"

    @property
    def has_any_block_hidden_from_homepage(self):
        for block in self.body:
            try:
                show_flag = block.value.get('show_on_homepage', None)
                if show_flag is False:
                    return True
            except AttributeError:
                continue
        return False

    def get_next_news_page(self):
        return NewsPage2.objects.live().public().specific().filter(
            Q(publish_date__lt=self.publish_date) |
            Q(publish_date=self.publish_date, id__lt=self.id)
        ).order_by('-publish_date', '-id').first()

    def get_previous_news_page(self):
        return NewsPage2.objects.live().public().specific().filter(
            Q(publish_date__gt=self.publish_date) |
            Q(publish_date=self.publish_date, id__gt=self.id)
        ).order_by('publish_date', 'id').first()

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['newspage'] = True
        context["prev_news"] = self.get_previous_news_page()
        context["next_news"] = self.get_next_news_page()
        return context
