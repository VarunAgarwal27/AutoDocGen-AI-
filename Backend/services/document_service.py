from utils.diagram_generator import generate_architecture_diagram
from utils.diagram_renderer import save_mermaid_file, render_mermaid_to_png
from utils.pdf_generator import generate_pdf

def generate_project_pdf(project_id: int, project_name: str, analysis: dict, docs: dict = None):
    base = f"uploads/output/{project_id}"

    mmd = f"{base}/architecture.mmd"
    png = f"{base}/architecture.png"
    pdf = f"{base}/report.pdf"

    code = generate_architecture_diagram(project_name, analysis)

    save_mermaid_file(code, mmd)
    render_mermaid_to_png(mmd, png)
    generate_pdf(pdf, png, docs)

    return pdf
