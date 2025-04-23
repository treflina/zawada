from django.urls import path
from .views import (
    get_pdf,
    new_menu,
    menu_detail_by_date,
    menu_detail_by_pk,
    MenuListView,
    MenuUpdateView,
    MenuDeleteView,
    # change_published_status
)

app_name = "menu"

urlpatterns = [
    path("lista/", MenuListView.as_view(), name="list"),
    path("data/", menu_detail_by_date, name="date-detail"),
    path("<int:pk>/", menu_detail_by_pk, name="detail"),
    # path("<int:pk>/", MenuDetailView.as_view(), name="detail"),
    path("nowy/", new_menu, name="create"),
    path("edytuj/<int:pk>/", MenuUpdateView.as_view(), name="update"),
    path("usun/<int:pk>/", MenuDeleteView.as_view(), name="delete"),
    # path("publikacja/<int:pk>/", change_published_status, name="publish"),
    path("pdf/<int:pk>/", get_pdf, name="pdf"),
]
