import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from app.products.models import Product
import random

class ExternalConnector:
    @staticmethod
    def sync_from_sailor(db: Session):
        # Mock logic: Pretend to scrape Sailor website
        # In real life, you'd use BeautifulSoup to parse their product list
        new_items = [
            {"name": "Sailor Premium Panjabi", "price": 2500, "sku": f"SLR-{random.randint(100,999)}"},
            {"name": "Sailor Linen Shirt", "price": 1800, "sku": f"SLR-{random.randint(100,999)}"}
        ]
        
        for item in new_items:
            existing = db.query(Product).filter(Product.sku == item['sku']).first()
            if not existing:
                new_prod = Product(
                    product_name=item['name'],
                    price=item['price'],
                    sku=item['sku'],
                    source_website="Sailor",
                    stock_quantity=random.randint(10, 50)
                )
                db.add(new_prod)
        db.commit()
        return f"Synced {len(new_items)} items from Sailor"

    @staticmethod
    def sync_from_rise(db: Session):
        # Simplified mock for Rise
        return "Synced 5 items from Rise"
