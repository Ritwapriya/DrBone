# ===========================================
# utils/report_generator.py
# ===========================================

import os
import re
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Import custom utils
from utils.ai_doctor import clean_text
from utils.pdf_styles import register_fonts, get_styles


# ---------- PDF Report Generator ----------
def create_pdf_report(report_data, img_clean_path, img_detailed_path, logo_path, output_pdf_path):
    """
    Creates a styled PDF report for fracture detection.

    Parameters:
    - report_data: list of dicts with Zone, Uncertainty (%), Shift (mm), Shape Diff, AI Doctor Notes
    - img_clean_path: path to YOLO clean output image
    - img_detailed_path: path to YOLO detailed output image
    - logo_path: hospital/clinic or app logo image path
    - output_pdf_path: final output PDF file path
    """

    # Load predefined styles
    styles_dict = get_styles()

    # Create PDF document
    doc = SimpleDocTemplate(output_pdf_path, pagesize=A4)
    story = []

    # ---------- FRONT PAGE ----------
    story.append(Paragraph("🧠 AI Doctor Fracture Analysis Report 🦴", styles_dict["title"]))
    story.append(Paragraph(f"📅 Date: {datetime.date.today().strftime('%B %d, %Y')}", styles_dict["date"]))
    story.append(Paragraph(
        "Welcome! This report summarizes detected fracture zones and AI-guided recommendations. "
        "Scroll through the pages for detailed analysis and images.",
        styles_dict["welcome"]
    ))

    # ---------- ADD LOGO ----------
    if logo_path and os.path.exists(logo_path):
        story.append(Image(logo_path, width=5 * inch, height=5 * inch))
    else:
        story.append(Paragraph("⚠️ Logo not found — skipping.", styles_dict["welcome"]))
    story.append(PageBreak())

    # ---------- TABLE + AI REPORTS ----------
    story.append(Paragraph(
        "📊 Fracture Detection Summary",
        ParagraphStyle('HeadingEmoji', parent=get_styles()['title'], fontName='EmojiFont')
    ))
    story.append(Spacer(1, 10))

    # Create summary table
    table_data = [["🦴 Zone", "📉 Uncertainty (%)", "📏 Shift (mm)", "🧩 Shape Diff"]]
    for entry in report_data:
        table_data.append([
            entry.get("Zone", "N/A"),
            entry.get("Uncertainty (%)", "N/A"),
            entry.get("Shift (mm)", "N/A"),
            entry.get("Shape Diff", "N/A")
        ])

    table = Table(table_data, hAlign='LEFT', colWidths=[2.2 * inch, 1.5 * inch, 1.5 * inch, 1.3 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'EmojiFont'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.7, colors.black),
    ]))
    story.append(table)

    # ---------- AI DOCTOR OBSERVATIONS ----------
    story.append(Spacer(1, 25))
    story.append(Paragraph(
        "🩺 AI Doctor Observations",
        ParagraphStyle('HeadingEmoji', parent=get_styles()['title'], fontName='EmojiFont')
    ))
    story.append(Spacer(1, 12))

    for entry in report_data:
        zone_header = f"🦴 <b>{entry.get('Zone', 'Unknown Zone')}</b>"
        summary_text = (
            f"<font color='darkblue'>📉 <b>Uncertainty:</b></font> {entry.get('Uncertainty (%)', 'N/A')}% &nbsp;&nbsp;"
            f"<font color='darkgreen'>📏 <b>Shift:</b></font> {entry.get('Shift (mm)', 'N/A')} mm &nbsp;&nbsp;"
            f"<font color='darkred'>🧩 <b>Shape Diff:</b></font> {entry.get('Shape Diff', 'N/A')}"
        )

        doctor_notes = clean_text(entry.get("AI Doctor Notes", ""))
        doctor_notes = re.sub(r"(Severity:)", "💢 <b>\\1</b>", doctor_notes)
        doctor_notes = re.sub(r"(Findings:)", "🔍 <b>\\1</b>", doctor_notes)
        doctor_notes = re.sub(r"(Advice:)", "💬 <b>\\1</b>", doctor_notes)
        doctor_notes = re.sub(r"(Nutrition Tip:)", "🥦 <b>\\1</b>", doctor_notes)
        doctor_notes = re.sub(r"(General Tip:)", "🌿 <b>\\1</b>", doctor_notes)
        doctor_notes = doctor_notes.replace("\n", "<br/>")

        card_table = Table(
            [[Paragraph(f"{zone_header}<br/><br/>{summary_text}<br/><br/>{doctor_notes}",
                        ParagraphStyle('CardStyle', fontName='EmojiFont', fontSize=10.5,
                                       leading=15, textColor=colors.black,
                                       spaceBefore=4, spaceAfter=4))]],
            colWidths=[6.5 * inch]
        )

        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(card_table)
        story.append(Spacer(1, 15))

    story.append(Paragraph(
        "➡️ Refer to the next pages for images",
        ParagraphStyle('NextPage', fontName='EmojiFont',
                       fontSize=12, textColor=colors.darkred,
                       alignment=TA_CENTER)
    ))
    story.append(PageBreak())

    # ---------- IMAGE SECTION ----------
    story.append(Paragraph("🩻 Detected Zones (Clean)",
                           ParagraphStyle('HeadingEmoji', parent=get_styles()['title'], fontName='EmojiFont')))
    if os.path.exists(img_clean_path):
        story.append(Image(img_clean_path, width=6 * inch, height=6 * inch))
    else:
        story.append(Paragraph("⚠️ Clean image not found.", get_styles()['welcome']))

    story.append(PageBreak())
    story.append(Paragraph("🔬 Detailed Fracture Analysis",
                           ParagraphStyle('HeadingEmoji', parent=get_styles()['title'], fontName='EmojiFont')))
    if os.path.exists(img_detailed_path):
        story.append(Image(img_detailed_path, width=6 * inch, height=6 * inch))
    else:
        story.append(Paragraph("⚠️ Detailed image not found.", get_styles()['welcome']))

    # ---------- BUILD PDF ----------
    doc.build(story)

    print(f"\n✅ Full report saved as {output_pdf_path}")
    print("💬 Summary table and AI Doctor insights are now on the same page — clean and professional.\n")

    return output_pdf_path
