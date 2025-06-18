from django.utils.html import format_html
from django.templatetags.static import static

from wagtail import hooks
from wagtail.admin.urls.collections import urlpatterns
from wagtail.admin.viewsets.base import ViewSet
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)
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


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/mywagtail.css"))


@hooks.register("register_icons")
def register_icons(icons):
    """Creates additional icons to use in editor's interface and templates"""
    return icons + [
        "home/exclamation.svg",
    ]


@hooks.register("register_rich_text_features")
def register_strong_feature(features):
    """
    Registering the `strong` feature. It will render bold text with `strong` tag.
    Default Wagtail uses the `b` tag.
    """
    feature_name = "strong"
    type_ = "STRONG"
    tag = "strong"

    # Configure how Draftail handles the feature in its toolbar.
    control = {
        "type": type_,
        "icon": "exclamation",
        "description": "Wyróżnienie ważnej treści",
        "style": {
            "font-weight": "bold",
        },
    }

    # Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Configure the content transform from the DB to the editor and back.
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: tag}},
    }

    # Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule("contentstate", feature_name, db_conversion)
