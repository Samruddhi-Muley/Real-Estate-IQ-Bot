# pdf_generator.py
# ------------------------------------------------
# Generates a downloadable PDF quiz report using
# the ReportLab library.
# Returns raw bytes so Streamlit can serve it
# directly as a download — no file saved to disk.
# ------------------------------------------------

import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


# ── Colour palette ───────────────────────────────────────────────────────
COLOR_DARK      = colors.HexColor("#1E293B")
COLOR_PRIMARY   = colors.HexColor("#4338CA")
COLOR_SUCCESS   = colors.HexColor("#065F46")
COLOR_SUCCESS_BG= colors.HexColor("#D1FAE5")
COLOR_DANGER    = colors.HexColor("#7F1D1D")
COLOR_DANGER_BG = colors.HexColor("#FEE2E2")
COLOR_INFO_BG   = colors.HexColor("#EFF6FF")
COLOR_INFO      = colors.HexColor("#1E3A5F")
COLOR_TIP_BG    = colors.HexColor("#FFFBEB")
COLOR_TIP       = colors.HexColor("#78350F")
COLOR_MUTED     = colors.HexColor("#64748B")
COLOR_BORDER    = colors.HexColor("#E2E8F0")


def _build_styles():
    """Returns a dict of all custom paragraph styles."""
    base = getSampleStyleSheet()

    styles = {}

    styles["title"] = ParagraphStyle(
        "title",
        fontSize=22, fontName="Helvetica-Bold",
        textColor=COLOR_DARK, alignment=TA_CENTER,
        spaceAfter=4
    )
    styles["subtitle"] = ParagraphStyle(
        "subtitle",
        fontSize=11, fontName="Helvetica",
        textColor=COLOR_MUTED, alignment=TA_CENTER,
        spaceAfter=2
    )
    styles["section"] = ParagraphStyle(
        "section",
        fontSize=13, fontName="Helvetica-Bold",
        textColor=COLOR_PRIMARY, spaceBefore=14, spaceAfter=6
    )
    styles["question"] = ParagraphStyle(
        "question",
        fontSize=10, fontName="Helvetica-Bold",
        textColor=COLOR_DARK, spaceBefore=10, spaceAfter=4,
        leading=14
    )
    styles["body"] = ParagraphStyle(
        "body",
        fontSize=9, fontName="Helvetica",
        textColor=COLOR_DARK, leading=13
    )
    styles["correct_label"] = ParagraphStyle(
        "correct_label",
        fontSize=9, fontName="Helvetica-Bold",
        textColor=COLOR_SUCCESS
    )
    styles["wrong_label"] = ParagraphStyle(
        "wrong_label",
        fontSize=9, fontName="Helvetica-Bold",
        textColor=COLOR_DANGER
    )
    styles["explanation"] = ParagraphStyle(
        "explanation",
        fontSize=9, fontName="Helvetica",
        textColor=COLOR_INFO, leading=13,
        leftIndent=8, rightIndent=8
    )
    styles["tip"] = ParagraphStyle(
        "tip",
        fontSize=9, fontName="Helvetica-Oblique",
        textColor=COLOR_TIP, leading=13,
        leftIndent=8, rightIndent=8
    )
    styles["footer"] = ParagraphStyle(
        "footer",
        fontSize=8, fontName="Helvetica",
        textColor=COLOR_MUTED, alignment=TA_CENTER
    )
    return styles


def _colored_cell(text, bg_color, text_color, bold=False):
    """Helper — returns a single-cell Table that acts as a colored box."""
    font = "Helvetica-Bold" if bold else "Helvetica"
    style = ParagraphStyle(
        "cell", fontSize=9, fontName=font,
        textColor=text_color, leading=13,
        leftIndent=6, rightIndent=6
    )
    t = Table([[Paragraph(text, style)]], colWidths=[155 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5,
         COLOR_SUCCESS if bg_color == COLOR_SUCCESS_BG else
         COLOR_DANGER  if bg_color == COLOR_DANGER_BG  else
         COLOR_PRIMARY),
    ]))
    return t


def generate_pdf(username: str, stats: dict) -> bytes:
    """
    Builds the full quiz report PDF and returns it as bytes.

    Args:
        username:  The logged-in user's name
        stats:     The dict returned by get_final_stats()

    Returns:
        Raw PDF bytes — pass directly to st.download_button(data=...)
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
    )

    S = _build_styles()
    story = []
    W = 174 * mm   # usable page width

    # ── Cover / Header ────────────────────────────────────────────────────
    story.append(Paragraph("🏠 RealEstate IQ Bot", S["title"]))
    story.append(Paragraph("Property Listings Assessment — Quiz Report", S["subtitle"]))
    story.append(Spacer(1, 3 * mm))

    now = datetime.now().strftime("%d %B %Y, %I:%M %p")
    story.append(Paragraph(f"Generated for <b>{username}</b> &nbsp;|&nbsp; {now}", S["subtitle"]))
    story.append(HRFlowable(width=W, thickness=1, color=COLOR_BORDER, spaceAfter=8))

    # ── Score summary table ───────────────────────────────────────────────
    accuracy = stats["accuracy"]
    if accuracy >= 90:
        grade = "A"
    elif accuracy >= 75:
        grade = "B"
    elif accuracy >= 60:
        grade = "C"
    else:
        grade = "D"

    summary_data = [
        ["Correct Answers", "Accuracy", "Grade", "Avg Score"],
        [
            f"{stats['correct']} / {stats['total_questions']}",
            f"{accuracy:.1f}%",
            grade,
            f"{stats['avg_score']:.0f} / 100",
        ],
    ]
    summary_table = Table(summary_data, colWidths=[W / 4] * 4)
    summary_table.setStyle(TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  COLOR_PRIMARY),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  9),
        ("BACKGROUND",   (0, 1), (-1, 1),  COLOR_INFO_BG),
        ("FONTNAME",     (0, 1), (-1, 1),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 1), (-1, 1),  13),
        ("TEXTCOLOR",    (0, 1), (-1, 1),  COLOR_DARK),
        ("ALIGN",        (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",   (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 0), (-1, -1), 7),
        ("GRID",         (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 4 * mm))

    # ── Topic breakdown table ─────────────────────────────────────────────
    story.append(Paragraph("Topic Breakdown", S["section"]))
    topic_rows = [["Topic", "Correct", "Total", "Score"]]
    for topic, data in stats["topic_scores"].items():
        pct = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        topic_rows.append([
            topic,
            str(data["correct"]),
            str(data["total"]),
            f"{pct:.0f}%"
        ])

    topic_table = Table(topic_rows, colWidths=[W * 0.55, W * 0.15, W * 0.15, W * 0.15])
    topic_style = [
        ("BACKGROUND",    (0, 0), (-1, 0),  COLOR_PRIMARY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 9),
        ("ALIGN",         (1, 0), (-1, -1), "CENTER"),
        ("ALIGN",         (0, 0), (0, -1),  "LEFT"),
        ("GRID",          (0, 0), (-1, -1), 0.5, COLOR_BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, COLOR_INFO_BG]),
    ]
    # highlight weak topics in red
    for row_i, (topic, data) in enumerate(stats["topic_scores"].items(), start=1):
        pct = (data["correct"] / data["total"]) if data["total"] > 0 else 0
        if pct < 0.6:
            topic_style.append(
                ("TEXTCOLOR", (0, row_i), (-1, row_i), COLOR_DANGER)
            )
            topic_style.append(
                ("FONTNAME",  (0, row_i), (-1, row_i), "Helvetica-Bold")
            )
    topic_table.setStyle(TableStyle(topic_style))
    story.append(topic_table)
    story.append(Spacer(1, 4 * mm))

    # ── Weak topics callout ───────────────────────────────────────────────
    if stats["weak_topics"]:
        weak_str = ", ".join(stats["weak_topics"])
        story.append(
            _colored_cell(
                f"⚠ Topics needing review: {weak_str}",
                COLOR_DANGER_BG, COLOR_DANGER, bold=True
            )
        )
        story.append(Spacer(1, 4 * mm))

    # ── Question-by-question review ───────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=1,
                             color=COLOR_BORDER, spaceAfter=4))
    story.append(Paragraph("Answer Review", S["section"]))

    for i, h in enumerate(stats["history"], 1):
        is_correct = h["is_correct"]

        # Question text
        story.append(Paragraph(
            f"Q{i}. {h['question']}",
            S["question"]
        ))

        # Result row
        if is_correct:
            story.append(_colored_cell(
                f"✓ Correct — {h['correct_answer']}",
                COLOR_SUCCESS_BG, COLOR_SUCCESS, bold=True
            ))
        else:
            story.append(_colored_cell(
                f"✗ Incorrect — Your answer: {h['user_answer']}  |  "
                f"Correct: {h['correct_answer']}",
                COLOR_DANGER_BG, COLOR_DANGER, bold=True
            ))

        story.append(Spacer(1, 2 * mm))

        # AI Explanation box
        story.append(_colored_cell(
            f"AI Explanation: {h['explanation']}",
            COLOR_INFO_BG, COLOR_INFO
        ))
        story.append(Spacer(1, 1.5 * mm))

        # Pro tip box
        story.append(_colored_cell(
            f"Pro Tip: {h['pro_tip']}",
            COLOR_TIP_BG, COLOR_TIP
        ))
        story.append(Spacer(1, 3 * mm))

    # ── Footer ────────────────────────────────────────────────────────────
    story.append(HRFlowable(width=W, thickness=1,
                             color=COLOR_BORDER, spaceBefore=6))
    story.append(Paragraph(
        "Generated by RealEstate IQ Bot · Powered by Groq AI (Llama 3.3 70B)",
        S["footer"]
    ))

    doc.build(story)
    return buffer.getvalue()