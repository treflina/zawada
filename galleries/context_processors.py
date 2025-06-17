from galleries.models import GalleriesIndexPage, GalleryPage
from menu.models import Menu

def latest_gallery_index_with_galleries(request):
    for index_page in GalleriesIndexPage.objects.live().order_by('-year__name'):
        if GalleryPage.objects.live().child_of(index_page).exists():
            index_page = index_page.specific
            return {'latest_gallery_index_url': index_page.url}
    return {'latest_gallery_index_url': None}


def get_newest_menu_pk(request):
    menu = Menu.objects.order_by("date_to").last()
    menu_pk = menu.id if menu else None
    return {'menu_pk': menu_pk }
