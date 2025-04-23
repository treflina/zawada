from django.forms import ModelForm, DateField, DateInput
from .models import Menu


class MenuForm(ModelForm):

    date_from = DateField(
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "mx-2 px-2 py-1 rounded-md border-2 \
                      border-slate-200 ",
            },
            format="%Y-%m-%d",
        ),
        label="From",
    )
    date_to = DateField(
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "flex items-center mx-2 px-2 py-1 rounded-md  \
                    border-2 border-slate-200 ",
            },
            format="%Y-%m-%d",
        ),
        label="To",
    )

    class Meta:
        model = Menu
        fields = "__all__"
