from wagtail.blocks import CharBlock, ListBlock, RichTextBlock, StreamBlock, StructBlock
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
        description = "Zdjęcie z opcjonalnym podpisem"


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
        help_text="Zacznij pisać, a następnie kliknij szybko dwukrotnie, aby otworzyć narzędzia edycji tekstu. " \
        "Jeśli chcesz przy wypunktowywaniu treści utworzyć listę w liście (podlistę) użyj klawisza TAB, Shift + TAB pozwala wrócić poziom wyżej." \
    )
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

