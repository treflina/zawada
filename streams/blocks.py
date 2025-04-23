from django.db import models

from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail import blocks


class TypedTableWithTextBlock(blocks.StreamBlock):
    title = blocks.CharBlock()
    table = TypedTableBlock([
        ('text', blocks.CharBlock()),
        ('rich_text', blocks.RichTextBlock()),
    ])
    paragraph = blocks.RichTextBlock()