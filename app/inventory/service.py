from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import pandas as pd
from app.products.models import Product
from app.orders.models import Order, OrderDetail
from app.inventory.schemas import StockAlert, DeadStockReport

class InventoryIntelligenceService:
    @staticmethod
    def get_stock_out_forecast(db: Session):
        # Calculate daily sales velocity for the last 14 days
        fourteen_days_ago = datetime.now() - timedelta(days=14)
        
        query = db.query(
            Product.id,
            Product.product_name,
            Product.stock_quantity,
            func.sum(OrderDetail.quantity).label('total_sales_14d')
        ).outerjoin(OrderDetail, Product.id == OrderDetail.product_id)\
         .outerjoin(Order, OrderDetail.order_id == Order.id)\
         .filter((Order.created_at >= fourteen_days_ago) | (OrderDetail.id == None))\
         .group_by(Product.id)\
         .all()
        
        forecasts = []
        for pid, name, stock, sales_14d in query:
            sales_14d = sales_14d or 0
            daily_velocity = sales_14d / 14 if sales_14d > 0 else 0
            
            if daily_velocity > 0:
                days_left = int(stock / daily_velocity)
                if days_left <= 7: # Alert if running out within a week
                    forecasts.append(StockAlert(
                        product_id=pid,
                        product_name=name,
                        current_stock=stock,
                        predicted_stock_out_days=days_left,
                        action_required="Order Now" if days_left <= 3 else "Monitor"
                    ))
            elif stock <= 5: # Basic low stock alert even without velocity
                forecasts.append(StockAlert(
                    product_id=pid,
                    product_name=name,
                    current_stock=stock,
                    predicted_stock_out_days=-1, # Unknown
                    action_required="Order Now"
                ))
        return forecasts

    @staticmethod
    def get_dead_stock_alerts(db: Session):
        # Find products with 0 sales in the last 30 days but positive stock
        thirty_days_ago = datetime.now() - timedelta(days=30)
        
        # Subquery for products sold in last 30 days
        sold_product_ids = db.query(OrderDetail.product_id)\
            .join(Order, OrderDetail.order_id == Order.id)\
            .filter(Order.created_at >= thirty_days_ago)\
            .distinct().all()
        sold_ids = [r[0] for r in sold_product_ids]
        
        dead_stock = db.query(Product)\
            .filter(~Product.id.in_(sold_ids))\
            .filter(Product.stock_quantity > 0)\
            .limit(10).all()
            
        reports = []
        for prod in dead_stock:
            reports.append(DeadStockReport(
                product_id=prod.id,
                product_name=prod.product_name,
                days_since_last_sale=30, # Minimal 30 days
                suggestion="Clearance Sale দিন অথবা সোশ্যাল মিডিয়াতে হাইলাইটস করুন।"
            ))
        return reports

    @classmethod
    def get_inventory_summary(cls, db: Session):
        return {
            "low_stock_items": cls.get_stock_out_forecast(db),
            "dead_stock_items": cls.get_dead_stock_alerts(db),
            "generated_at": datetime.now()
        }
