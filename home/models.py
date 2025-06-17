from wagtail.models import Page

from core.models import EventSnippet


class HomePage(Page):

    template = "home/home_page.html"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["events"] = EventSnippet.objects.all().order_by("date")
        context["home_page"] = "active"
        return context
