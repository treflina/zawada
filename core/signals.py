
from django.db.models.signals import post_save
from django.utils.text import slugify

from wagtail.models import Collection

from galleries.models import GalleriesIndexPage
from home.models import HomePage
from .models import SchoolYearSnippet



def create_collection_and_galleries_page(sender, instance, created, **kwargs):
    if instance and created:
        coll = Collection.objects.filter(name=f"Galerie - {instance.name}").last()
        if not coll:
            new_coll = Collection(name=f"Galerie - {instance.name}")
            root_coll = Collection.get_first_root_node()
            root_coll.add_child(instance=new_coll)
            root_coll.save()

        gall = GalleriesIndexPage.objects.filter(title=f"Galerie zdjęć- {instance.name}").last()
        if not gall:
            home_page = HomePage.objects.last()
            if home_page:
                new_gall = GalleriesIndexPage(
                    title = f"Galerie zdjęć - {instance.name}",
                    slug = f"galerie{slugify(instance.name)}",
                    year=instance,
                )
                home_page.add_child(instance=new_gall)


post_save.connect(create_collection_and_galleries_page, sender=SchoolYearSnippet)



