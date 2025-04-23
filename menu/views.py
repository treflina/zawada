from datetime import datetime
from io import BytesIO
from django import forms
from django.http import FileResponse, HttpResponse
from django_htmx.http import trigger_client_event
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    ListView,
    UpdateView,
)
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table

from .filters import BaseFilter
from .forms import MenuForm
from .models import Menu
from .utils.pdf_styles import get_styles, linebreak


class MenuListView(ListView):
    model = Menu
    template_name = "menu/menu_list.html"
    context_object_name = "menu_list"

    def get_queryset(self):
        self.filterset = BaseFilter(
            self.request.GET, queryset=super().get_queryset()
            )
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset
        return context


def menu_detail_by_pk(request, pk):
    """Menu detail view."""
    menu = get_object_or_404(Menu, pk=pk)

    next_menu = (
        Menu.objects.filter(
            date_from__gt=menu.date_from
            ).order_by("date_from").first()
    )
    prev_menu = Menu.objects.filter(date_from__lt=menu.date_from).first()

    context = {"menu": menu, "next": next_menu, "prev": prev_menu}

    if request.htmx:
        return render(request, "menu/partials/menu_detail_partial.html", context)
    return render(request, "menu/menu_detail.html", context)


def menu_detail_by_date(request):
    """Menu detail view."""
    context = {}
    try:
        submitted_date = forms.DateField().clean(request.GET.get("selected_date"))
        selected_date = datetime.strftime(submitted_date, "%Y-%m-%d")
        menu = (
            Menu.objects.filter(date_from__lte=selected_date)
            .filter(date_to__gte=selected_date)
            .last()
        )
        if menu:
            next_menu = (
                Menu.objects.filter(date_from__gt=menu.date_from)
                .order_by("date_from")
                .first()
            )
            prev_menu = Menu.objects.filter(date_from__lt=menu.date_from).first()
            context.update({"next": next_menu, "prev": prev_menu})

    except forms.ValidationError:
        menu = None

    context["menu"] = menu

    if request.htmx:
        return render(request, "menu/partials/menu_detail_partial.html", context)
    return render(request, "menu/menu_detail.html", context)


def new_menu(request):
    form = MenuForm()
    context = {}
    context["form"] = form
    context["creating"] = True
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            new_menu = form.save()
            return render(request, "menu/menu_detail.html", {"menu": new_menu})
    return render(request, "menu/menu_form.html", context)


class MenuUpdateView(UpdateView):
    """Menu update view."""

    model = Menu
    form_class = MenuForm
    template_name = "menu/menu_form.html"
    success_url = reverse_lazy("menu:list")
    context_object_name = "menu"


class MenuDeleteView(DeleteView):
    model = Menu
    success_url = reverse_lazy("menu:list")  # unused in HTMX case

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()

        # Send a 204 No Content response with an HX-Trigger header
        response = HttpResponse(status=204)
        response = trigger_client_event(response, "menuDeleted")
        return response


# def change_published_status(request, pk):
#     """Change published status of menu."""
#     menu = Menu.objects.get(pk=pk)
#     menu.published = not menu.published
#     menu.save()
#     response = HttpResponse(status=204)
#     response = trigger_client_event(response, 'menuChanged')
#     return response


def get_pdf(request, pk):

    menu = Menu.objects.get(id=pk)
    date_from = menu.date_from.strftime("%d.%m.")
    date_to = menu.date_to.strftime("%d.%m.%Y")

    pdf_buffer = BytesIO()

    normalStyle, headingStyle, style, style_table = get_styles()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(A4),
        rightMargin=25,
        leftMargin=25,
        topMargin=15,
        bottomMargin=15,
    )
    data = [
        [
            Paragraph("", headingStyle),
            Paragraph("Śniadanie", headingStyle),
            Paragraph("II Śniadanie", headingStyle),
            Paragraph("Zupa", headingStyle),
            Paragraph("II danie", headingStyle),
            Paragraph("Podwieczorek", headingStyle),
        ]
    ]

    monday = [
        Paragraph("Poniedziałek", normalStyle),
        Paragraph(linebreak(menu.breakfast1), normalStyle),
        Paragraph(linebreak(menu.snack1), normalStyle),
        Paragraph(linebreak(menu.soup1), normalStyle),
        Paragraph(linebreak(menu.main1), normalStyle),
        Paragraph(linebreak(menu.dessert1), normalStyle),
    ]
    tuesday = [
        Paragraph("Wtorek", normalStyle),
        Paragraph(linebreak(menu.breakfast2), normalStyle),
        Paragraph(linebreak(menu.snack2), normalStyle),
        Paragraph(linebreak(menu.soup2), normalStyle),
        Paragraph(linebreak(menu.main2), normalStyle),
        Paragraph(linebreak(menu.dessert2), normalStyle),
    ]
    wednesday = [
        Paragraph("Środa", normalStyle),
        Paragraph(linebreak(menu.breakfast3), normalStyle),
        Paragraph(linebreak(menu.snack3), normalStyle),
        Paragraph(linebreak(menu.soup3), normalStyle),
        Paragraph(linebreak(menu.main3), normalStyle),
        Paragraph(linebreak(menu.dessert3), normalStyle),
    ]
    thursday = [
        Paragraph("Czwartek", normalStyle),
        Paragraph(linebreak(menu.breakfast4), normalStyle),
        Paragraph(linebreak(menu.snack4), normalStyle),
        Paragraph(linebreak(menu.soup4), normalStyle),
        Paragraph(linebreak(menu.main4), normalStyle),
        Paragraph(linebreak(menu.dessert4), normalStyle),
    ]
    friday = [
        Paragraph("Piątek", normalStyle),
        Paragraph(linebreak(menu.breakfast5), normalStyle),
        Paragraph(linebreak(menu.snack5), normalStyle),
        Paragraph(linebreak(menu.soup5), normalStyle),
        Paragraph(linebreak(menu.main5), normalStyle),
        Paragraph(linebreak(menu.dessert5), normalStyle),
    ]
    data.append(monday)
    data.append(tuesday)
    data.append(wednesday)
    data.append(thursday)
    data.append(friday)

    table = Table(
        data,
        spaceBefore=20,
        colWidths=[30 * mm, 55 * mm, 35 * mm, 45 * mm, 55 * mm, 50 * mm],
        minRowHeights=[5 * mm, 20 * mm, 20 * mm, 20 * mm, 20 * mm, 20 * mm],
    )

    elems = []
    elems.append(Paragraph((f"Jadłospis od {date_from} do {date_to}"), style=style))
    elems.append(Spacer(1, 6))
    elems.append(table)

    table.setStyle(style_table)

    doc.build(elems)
    pdf_buffer.seek(0)
    return FileResponse(
        pdf_buffer, as_attachment=False, filename=f"Jadlospis_{menu.date_from}.pdf"
    )
