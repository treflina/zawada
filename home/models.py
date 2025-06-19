from wagtail.models import Page

from core.models import EventSnippet
from news.models import NewsIndexPage, NewsPage2


class HomePage(Page):

    template = "home/home_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["events"] = EventSnippet.objects.all().order_by("date")
        context["home_page"] = "active"
        context["news_index_page"] = NewsIndexPage.objects.live().public().specific().first()
        context["newspages"] = NewsPage2.objects.live().public().specific() \
                        .order_by("-publish_date", "-id")[:3]
        return context
