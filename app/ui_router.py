from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, desc
from app.database import get_db
from app.insights.service import InsightService
from app.inventory.service import InventoryIntelligenceService
from sqlalchemy import func
from app.orders.models import Order, OrderDetail
from app.users.models import User, UserAddress
from app.products.models import Product

router = APIRouter(tags=["UI"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    # Fetch data for the dashboard
    insights = InsightService.get_all_insights(db)
    inventory = InventoryIntelligenceService.get_inventory_summary(db)
    
    # Simple stats
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
    total_orders = db.query(Order).count()
    
    # Regional Sales Data for Chart
    region_data = db.query(
        UserAddress.district,
        func.count(Order.id).label('order_count')
    ).join(User, UserAddress.user_id == User.id)\
     .join(Order, User.id == Order.user_id)\
     .group_by(UserAddress.district)\
     .order_by(desc('order_count'))\
     .limit(5).all()
    
    # Top Products Data for Chart
    top_products = db.query(
        Product.product_name,
        func.sum(OrderDetail.quantity).label('qty_sold')
    ).join(OrderDetail, Product.id == OrderDetail.product_id)\
     .group_by(Product.id)\
     .order_by(desc('qty_sold'))\
     .limit(5).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "title": "মার্চেন্ট ড্যাশবোর্ড",
        "insights": insights,
        "inventory": inventory,
        "stats": {
            "total_revenue": total_revenue,
            "total_orders": total_orders
        },
        "charts": {
            "regions": [r[0] or "Unknown" for r in region_data],
            "region_counts": [r[1] for r in region_data],
            "products": [p[0] for p in top_products],
            "product_counts": [p[1] for p in top_products]
        }
    })

@router.get("/chat")
async def chatbot_page(request: Request):
    return templates.TemplateResponse("chatbot.html", {
        "request": request,
        "title": "এআই চ্যাট সাপোর্ট"
    })

@router.get("/profile")
async def profile_page(request: Request, db: Session = Depends(get_db)):
    # Fetch first user as the 'logged in' merchant for demonstration
    user = db.query(User).first()
    
    if not user:
        # Create a mock user if database is empty for UI testing
        user = {
            "id": "M-101",
            "name": "ব্যবসায়ী ভাই (Demo)",
            "email": "merchant@example.com",
            "phone": "017XXXXXXXX",
            "source_website": "Sailor / Rise",
            "addresses": [{"city": "ঢাকা", "district": "মিরপুর", "address": "সেকশন-১০, ঢাকা"}]
        }

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "title": "আমার প্রোফাইল",
        "user": user
    })
