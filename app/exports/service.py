import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os

class ExportService:
    @staticmethod
    def generate_excel_report(data: list, filename: str = "report.xlsx"):
        df = pd.DataFrame(data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='AI Insights')
        output.seek(0)
        return output

    @staticmethod
    def generate_pdf_report(insights: list):
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "EcomPredictor - AI Business Report")
        
        p.setFont("Helvetica", 12)
        y = 700
        for item in insights:
            if y < 100:
                p.showPage()
                y = 750
            p.drawString(100, y, f"- {item['title']}: {item['message'][:80]}...")
            y -= 30
            
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
