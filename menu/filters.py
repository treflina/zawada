import operator
from functools import reduce

import django_filters
from django.db.models import Q
from django.forms import TextInput


# Custom widget that uses search input type
class SearchInput(TextInput):
    input_type = "search"


class BaseFilter(django_filters.FilterSet):

    query = django_filters.CharFilter(
        method="menu_search",
        label="Znajdź potrawę",
        widget=SearchInput(
            attrs={
                "placeholder": "Wyszukaj...",
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm \
            rounded-l-lg focus:ring-blue-500 \
            focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700  \
            dark:border-gray-600 dark:placeholder-gray-400 dark:text-white \
            dark:focus:ring-blue-500 dark:focus:border-blue-500",
            }
        ),
    )

    def menu_search(self, queryset, name, value):
        query_words = value.split()

        return queryset.filter(
            reduce(
                operator.and_,
                (
                    Q(breakfast1__icontains=word)
                    | Q(breakfast2__icontains=word)
                    | Q(breakfast3__icontains=word)
                    | Q(breakfast4__icontains=word)
                    | Q(breakfast5__icontains=word)
                    | Q(snack1__icontains=word)
                    | Q(snack2__icontains=word)
                    | Q(snack3__icontains=word)
                    | Q(snack4__icontains=word)
                    | Q(snack5__icontains=word)
                    | Q(dessert1__icontains=word)
                    | Q(dessert2__icontains=word)
                    | Q(dessert3__icontains=word)
                    | Q(dessert4__icontains=word)
                    | Q(dessert5__icontains=word)
                    | Q(soup1__icontains=word)
                    | Q(soup2__icontains=word)
                    | Q(soup3__icontains=word)
                    | Q(soup4__icontains=word)
                    | Q(soup5__icontains=word)
                    | Q(main1__icontains=word)
                    | Q(main2__icontains=word)
                    | Q(main3__icontains=word)
                    | Q(main4__icontains=word)
                    | Q(main5__icontains=word)
                    for word in query_words
                ),
            )
        )
