from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, func

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    barcode = Column(String(100), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    variant = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    stock_quantity = Column(Integer, default=0)
    min_stock_level = Column(Integer, default=5)
    source_website = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class ProductReview(Base):
    __tablename__ = "product_reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    customer_name = Column(String(100))
    rating = Column(Integer)
    review_text = Column(Text)
    sentiment_label = Column(String(20)) # 'positive', 'negative', 'neutral'
    created_at = Column(DateTime, default=func.now())
