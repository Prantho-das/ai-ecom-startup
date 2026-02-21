from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.exports.service import ExportService
from app.connectors.service import ExternalConnector
from app.insights.service import InsightService

from app.reviews.service import SentimentService

router = APIRouter(prefix="/admin", tags=["Admin Operations"])

@router.get("/sentiment/{product_id}")
def analyze_product_sentiment(product_id: int, db: Session = Depends(get_db)):
    result = SentimentService.analyze_reviews(db, product_id)
    return {"analysis": result}

@router.get("/export/excel")
def export_insights_excel(db: Session = Depends(get_db)):
    insights = InsightService.get_all_insights(db)
    # Flatten insights for excel
    data = [{"Title": i.title, "Message": i.message, "Category": i.category} for i in insights]
    file = ExportService.generate_excel_report(data)
    return StreamingResponse(
        file, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=ai_insights.xlsx"}
    )

@router.get("/export/pdf")
def export_insights_pdf(db: Session = Depends(get_db)):
    insights = InsightService.get_all_insights(db)
    data = [{"title": i.title, "message": i.message} for i in insights]
    file = ExportService.generate_pdf_report(data)
    return StreamingResponse(
        file, 
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=ai_business_report.pdf"}
    )

@router.post("/sync/sailor")
def sync_sailor(db: Session = Depends(get_db)):
    result = ExternalConnector.sync_from_sailor(db)
    return {"message": result}
