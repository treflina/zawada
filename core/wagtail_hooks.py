from wagtail import hooks
from wagtail.admin.urls.collections import urlpatterns
from wagtail.admin.viewsets.base import ViewSet
from wagtail.models import Collection
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from .models import EventSnippet, SchoolYearSnippet


class SchoolYearViewSet(SnippetViewSet):

    model = SchoolYearSnippet
    icon = "date"
    menu_label = "Rok szkolny"
    menu_order = 280
    add_to_admin_menu = True

register_snippet(SchoolYearSnippet, viewset=SchoolYearViewSet)


class EventsViewSet(SnippetViewSet):

    model = EventSnippet
    icon = "date"
    menu_label = "Wydarzenia"
    menu_order = 270
    add_to_admin_menu = True

register_snippet(EventSnippet, viewset=EventsViewSet)


class CustomCollectionViewSet(ViewSet):

    model = Collection
    name = "collections"
    menu_label = "Kolekcje"
    menu_order = 290
    icon = "folder"
    add_to_admin_menu = True
    add_to_settings_menu = False


    def get_urlpatterns(self):
        return urlpatterns


@hooks.register("register_admin_viewset")
def register_viewset():
    return CustomCollectionViewSet()