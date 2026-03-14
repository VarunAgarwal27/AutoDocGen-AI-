from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(output_path: str, diagram_path: str, docs: dict = None):
    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(output_path)

    story = []
    story.append(Paragraph("AutoDocGen Project Report", styles["Title"]))

    if docs:
        for key, value in docs.items():
            story.append(Paragraph(key.upper(), styles["Heading2"]))

            if isinstance(value, list):
                for item in value:
                    story.append(Paragraph(f"- {item}", styles["Normal"]))
            else:
                story.append(Paragraph(str(value), styles["Normal"]))

            story.append(Spacer(1, 12))

    story.append(Paragraph("System Architecture Diagram", styles["Heading2"]))
    img = Image(diagram_path, width=400, height=300)
    story.append(img)

    doc.build(story)
