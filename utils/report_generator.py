from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf_report(name, email, phone, education, skills, score, predicted_role):
    """
    Builds a formatted PDF resume-analysis report in memory and
    returns the raw PDF bytes (ready for st.download_button).
    """
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        textColor=colors.grey,
        spaceAfter=20,
    )
    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        spaceBefore=16,
        spaceAfter=8,
    )

    story = []

    story.append(Paragraph("AI Resume Analysis Report", title_style))
    story.append(
        Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            subtitle_style,
        )
    )

    # --- Candidate info table ---
    story.append(Paragraph("Candidate Information", section_style))
    info_data = [
        ["Name", name or "Not Found"],
        ["Email", email or "Not Found"],
        ["Phone", phone or "Not Found"],
        ["Education", ", ".join(education) if education else "Not Found"],
    ]
    info_table = Table(info_data, colWidths=[1.5 * inch, 4.5 * inch])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(info_table)

    # --- Skills ---
    story.append(Paragraph("Skills Detected", section_style))
    skills_text = ", ".join(skills) if skills else "No matching skills found."
    story.append(Paragraph(skills_text, styles["Normal"]))

    # --- Results ---
    story.append(Paragraph("Analysis Results", section_style))
    results_data = [
        ["Resume Score", f"{score}/100"],
        ["Predicted Job Role", predicted_role or "Not Available"],
    ]
    results_table = Table(results_data, colWidths=[1.5 * inch, 4.5 * inch])
    results_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(results_table)

    story.append(Spacer(1, 24))
    story.append(
        Paragraph(
            "Generated automatically by AI Resume Analyzer.",
            ParagraphStyle("Footer", parent=styles["Normal"], textColor=colors.grey, fontSize=8),
        )
    )

    doc.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
