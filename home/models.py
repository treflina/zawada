from django.db import models

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page



class HomePage(Page):

    template = "home/home_page.html"

