from django.db import models
from django.utils.translation import gettext_lazy as _
from django_prose_editor.fields import ProseEditorField


class Menu(models.Model):

    date_from = models.DateField(_("From"))
    date_to = models.DateField(_("To"))
    published = models.BooleanField(_("Published"), default=False)
    breakfast1 = ProseEditorField(
        _("Breakfast on Monday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    breakfast2 = ProseEditorField(
        _("Breakfast on Tuesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    breakfast3 = ProseEditorField(
        _("Breakfast on Wednesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    breakfast4 = ProseEditorField(
        _("Breakfast on Thursday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    breakfast5 = ProseEditorField(
        _("Breakfast on Friday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    snack1 = ProseEditorField(
        _("Snack on Monday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    snack2 = ProseEditorField(
        _("Snack on Tuesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    snack3 = ProseEditorField(
        _("Snack on Wednesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    snack4 = ProseEditorField(
        _("Snack on Thursday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    snack5 = ProseEditorField(
        _("Snack on Friday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    soup1 = ProseEditorField(
        _("Soup on Monday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    soup2 = ProseEditorField(
        _("Soup on Tuesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    soup3 = ProseEditorField(
        _("Soup on Wednesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    soup4 = ProseEditorField(
        _("Soup on Thursday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    soup5 = ProseEditorField(
        _("Soup on Friday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    main1 = ProseEditorField(
        _("Main on Monday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    main2 = ProseEditorField(
        _("Main on Tuesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    main3 = ProseEditorField(
        _("Main on Wednesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    main4 = ProseEditorField(
        _("Main on Thursday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    main5 = ProseEditorField(
        _("Main on Friday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    dessert1 = ProseEditorField(
        _("Dessert on Monday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    dessert2 = ProseEditorField(
        _("Dessert on Tuesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    dessert3 = ProseEditorField(
        _("Dessert on Wednesday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    dessert4 = ProseEditorField(
        _("Dessert on Thursday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )
    dessert5 = ProseEditorField(
        _("Dessert on Friday"),
        null=True,
        blank=True,
        config={
            "types": [
                "strong",
            ],
            "history": True,
        },
    )

    def __str__(self):
        return f"Menu {self.date_from} - {self.date_to}"

    class Meta:
        ordering = ["-date_from"]
