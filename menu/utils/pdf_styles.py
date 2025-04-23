from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet, TA_CENTER
from reportlab.platypus import TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.contrib.staticfiles import finders


def linebreak(value):
    return value.replace("</p>", "</p><br />")


def get_styles():
    """Get styles for PDF."""

    font_normal = finders.find("fonts/Roboto-Regular.ttf")
    font_medium = finders.find("fonts/Roboto-Medium.ttf")

    pdfmetrics.registerFont(TTFont("roboto", font_normal))
    pdfmetrics.registerFont(TTFont("roboto-medium", font_medium))
    pdfmetrics.registerFontFamily("roboto", normal="roboto", bold="roboto-medium")

    normalStyle = ParagraphStyle(
        name="Normal",
        fontName="roboto",
        fontSize=12,
    )

    stylesheet = getSampleStyleSheet()
    headingStyle = stylesheet["Heading4"]
    headingStyle.fontName = "roboto-medium"
    headingStyle.fontSize = 12

    style = ParagraphStyle(
        name="Title",
        fontName="roboto-medium",
        fontSize=14,
        alignment=TA_CENTER,
    )

    style_table = TableStyle(
        [
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("FONTNAME", (0, 0), (-1, 0), "roboto-medium"),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("FONTNAME", (1, -1), (-1, 1), "roboto"),
        ]
    )
    return normalStyle, headingStyle, style, style_table
