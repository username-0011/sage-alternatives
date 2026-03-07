from pathlib import Path
from fpdf import FPDF

class DarkPDF(FPDF):
    def header(self):
        self.set_fill_color(10, 15, 13)
        self.rect(0, 0, 210, 297, style="F")

class ReportService:
    def __init__(self, report_dir: Path) -> None:
        self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)
        # Point to the font file you copied into the app directory
        self.font_path = Path(__file__).parent / "arial.ttf"

    def generate(self, result: dict) -> Path:
        pdf = DarkPDF()
        
        # Register the Unicode font (using the same file for regular and bold for simplicity)
        pdf.add_font("CustomFont", "", str(self.font_path))
        pdf.add_font("CustomFont", "B", str(self.font_path))

        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_text_color(34, 197, 94)
        pdf.set_font("CustomFont", "B", 24)
        pdf.cell(0, 12, "GreenBuild AI Report", ln=True)

        pdf.set_text_color(245, 247, 245)
        pdf.set_font("CustomFont", "", 12)
        pdf.cell(0, 8, result["project_name"], ln=True)
        pdf.cell(0, 8, result["request"]["location"], ln=True)
        pdf.ln(4)

        pdf.set_font("CustomFont", "B", 15)
        pdf.cell(0, 8, "Executive Summary", ln=True)
        pdf.set_font("CustomFont", "", 11)
        pdf.multi_cell(0, 7, result["executive_summary"])
        pdf.ln(3)

        metrics = result["summary_metrics"]
        pdf.set_font("CustomFont", "B", 15)
        pdf.cell(0, 8, "Portfolio Metrics", ln=True)
        pdf.set_font("CustomFont", "", 11)
        pdf.multi_cell(
            0,
            7,
            (
                f"Carbon Reduction: {metrics['total_estimated_carbon_reduction_pct']}%\n"
                f"Cost Delta: {metrics['average_cost_delta_pct']}%\n"
                f"Speed Delta: {metrics['average_delivery_speed_delta_pct']}%\n"
                f"Sustainability Score: {metrics['average_sustainability_score']}"
            ),
        )
        pdf.ln(3)

        for component in result["components"]:
            top = component["alternatives"][0]
            pdf.set_text_color(34, 197, 94)
            pdf.set_font("CustomFont", "B", 13)
            pdf.cell(0, 8, component["component"], ln=True)
            pdf.set_text_color(245, 247, 245)
            pdf.set_font("CustomFont", "", 10)
            pdf.multi_cell(
                0,
                6,
                (
                    f"Baseline: {component['baseline']}\n"
                    f"Top Alternative: {top['name']}\n"
                    f"Carbon: {top['carbon_reduction_pct']}% | Cost: {top['cost_delta_pct']}% | "
                    f"Speed: {top['speed_delta_pct']}% | Score: {top['sustainability_score']}\n"
                    f"Why: {top['rationale']}"
                ),
            )
            pdf.ln(2)

        report_path = self.report_dir / f"{result['slug']}.pdf"
        pdf.output(str(report_path))
        return report_path