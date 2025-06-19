from wagtail.blocks import (
    BooleanBlock,
    CharBlock,
    ListBlock,
    RichTextBlock,
    StreamBlock,
    StructBlock
)
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


custom_table_options = {
   'contextMenu': {
      'items': {
        "row_above": {
          'name': 'Wstaw wiersz powyżej',
        },
        "row_below": {
          'name': 'Wstaw wiersz poniżej',
        },
        "col_left": {
          'name': 'Wstaw kolumnę z lewej',
        },
        "col_right": {
          'name': 'Wstaw kolumnę z prawej',
        },
        "remove_row": {
          'name': 'Usuń wiersz',
        },
        "remove_col": {
          'name': 'Usuń kolumnę',
        },
        "---------": {
          'name': "---------",
        },
        "undo": {
          'name': 'Cofnij',
        },
        "redo": {
          'name': 'Powtórz',
        }
      }
    }
}


class CaptionedImageBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption
    """

    image = ImageChooserBlock(label="Zdjęcie", required=True)
    caption = CharBlock(label="Opcjonalny podpis zdjęcia", required=False)

    class Meta:
        icon = "image"
        template = "blocks/captioned_image_block.html"
        label = "Zdjęcie"

class CaptionedImageWithFlagBlock(StructBlock):
    """
    Custom `StructBlock` for utilizing images with associated caption
    """

    image = ImageChooserBlock(label="Zdjęcie", required=True)
    caption = CharBlock(label="Opcjonalny podpis zdjęcia", required=False)
    show_on_homepage = BooleanBlock(required=False, default=False)

    class Meta:
        icon = "image"
        template = "blocks/caption_image_block.html"
        label = "Zdjęcie"


class ParagraphWithFlagBlock(StructBlock):
    paragraph_block = RichTextBlock(
        label="Treść",
        features=[
            "bold",
            "strong",
            "italic",
            "ol",
            "ul",
            "link",
            "document-link",
        ],
        help_text="""Zacznij pisać, a następnie kliknij szybko dwukrotnie, aby otworzyć narzędzia edycji tekstu.
Jeśli chcesz przy wypunktowywaniu treści utworzyć listę w liście (podlistę) użyj klawisza TAB,
Shift + TAB pozwala wrócić poziom wyżej.""")

    show_on_homepage = BooleanBlock(
        label="Widoczne na stronie głównej",
        required=False,
        default=False
        )

    class Meta:
        template = "blocks/paragraph_with_flag.html"
        icon = "doc-full"
        label = "Tekst"


class HeadingWithFlagBlock(StructBlock):
    heading = CharBlock(label="Podtytuł")
    show_on_homepage = BooleanBlock(
        label="Widoczne na stronie głównej",
        required=False,
        default=False
        )

    class Meta:
        label="Podtytuł"
        template="blocks/heading_with_flag.html"


class TableWithFlagBlock(StructBlock):
    table = TableBlock(
        label="Tabela",
        table_options=custom_table_options,
    )
    show_on_homepage = BooleanBlock(
        label="Widoczne na stronie głównej",
        required=False,
        default=False
        )

    class Meta:
        label="Tabela"
        template="blocks/table_with_flag.html"


class DocsWithFlagBlock(StructBlock):
    docs = ListBlock(
        DocumentChooserBlock(),
        label = "Dokumenty do pobrania"
    )
    show_on_homepage = BooleanBlock(
        label="Widoczne na stronie głównej",
        required=False,
        default=False
        )

    class Meta:
        label="Dokumenty do pobrania"
        template="blocks/documents_with_flag.html"


class BaseStreamBlock(StreamBlock):
    """
    Define the custom blocks that `StreamField` will utilize
    """

    paragraph_block = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        features=[
            "bold",
            "strong",
            "italic",
            "ol",
            "ul",
            "link",
            "document-link",
        ],
        label="Tekst",
        help_text="""Zacznij pisać, a następnie kliknij szybko dwukrotnie, aby otworzyć narzędzia edycji tekstu.
Jeśli chcesz przy wypunktowywaniu treści utworzyć listę w liście (podlistę) użyj klawisza TAB,
Shift + TAB pozwala wrócić poziom wyżej.""")
    heading = CharBlock(
        required=False,
        label="Podtytuł",
        template="blocks/heading_block.html"
        )
    image_block = CaptionedImageBlock(
        required=False,
        label="Zdjęcie",
        template="blocks/caption_image_block.html",
    )
    table = TableBlock(
        required=False,
        label="Tabela",
        template="blocks/table_block.html",
        table_options=custom_table_options,
    )
    docs = ListBlock(
        DocumentChooserBlock(),
        required=False,
        label="Dokumenty do pobrania",
        template="blocks/documents_block.html",
    )

class BaseStreamWithFlagBlock(StreamBlock):
    """
    Blocks with show_on_homepage flag definition
    """

    paragraph_block = ParagraphWithFlagBlock(required=False)
    heading = HeadingWithFlagBlock(required=False)
    image_block = CaptionedImageWithFlagBlock(required=False)
    table = TableWithFlagBlock(required=False)
    docs = DocsWithFlagBlock(required=False)
