from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def register_fonts(font_path):
    pdfmetrics.registerFont(TTFont('EmojiFont', font_path))

def get_styles():
    styles = getSampleStyleSheet()
    return {
        "title": ParagraphStyle('TitleStyle', parent=styles['Title'], fontName='EmojiFont',
                                fontSize=30, alignment=TA_CENTER, textColor=colors.darkblue, spaceAfter=20),
        "date": ParagraphStyle('DateStyle', parent=styles['Normal'], fontName='EmojiFont',
                               fontSize=14, alignment=TA_CENTER, textColor=colors.white,
                               backColor=colors.darkblue, spaceAfter=30, leading=18),
        "welcome": ParagraphStyle('WelcomeStyle', parent=styles['Normal'], fontName='EmojiFont',
                                  fontSize=12, alignment=TA_CENTER, textColor=colors.darkgreen,
                                  spaceAfter=50, leading=18),
    }
