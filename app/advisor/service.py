import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.orders.models import Order, OrderDetail
from app.products.models import Product
from app.users.models import User, UserAddress
from datetime import datetime, timedelta

from app.utils.cache import cache_instance

# Configure Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = None

class AdvisorService:
    @staticmethod
    def get_business_context(db: Session, force_refresh: bool = False):
        # Cache context for 15 minutes
        cache_key = "business_context_summary"
        if not force_refresh:
            cached_context = cache_instance.get(cache_key)
            if cached_context:
                return cached_context

        # Fetch key metrics for context
        total_orders = db.query(Order).count()
        total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0
        
        # Region stats
        region_stats = db.query(
            UserAddress.district, 
            func.count(Order.id).label('order_count'),
            func.sum(Order.total_amount).label('revenue')
        ).join(User, UserAddress.user_id == User.id)\
         .join(Order, User.id == Order.user_id)\
         .group_by(UserAddress.district)\
         .order_by(desc('revenue'))\
         .limit(3).all() # Reduced from 5 to 3 to save tokens
        
        # Product stats
        top_products = db.query(
            Product.product_name,
            func.sum(OrderDetail.quantity).label('qty_sold')
        ).join(OrderDetail, Product.id == OrderDetail.product_id)\
         .group_by(Product.id)\
         .order_by(desc('qty_sold'))\
         .limit(3).all() # Reduced from 5 to 3 to save tokens

        context = f"Orders:{total_orders}, Rev:{total_revenue}. "
        context += "Top Regions: " + ", ".join([f"{r[0]}({r[1]} orders)" for r in region_stats]) + ". "
        context += "Top Prods: " + ", ".join([f"{p[0]}({p[1]} sold)" for p in top_products])
        
        cache_instance.set(cache_key, context, ttl_seconds=900) # 15 mins cache
        return context

    @staticmethod
    def ask_advisor(db: Session, query: str):
        if not model:
            return "দুঃখিত, এআই অ্যাডভাইজার এই মুহূর্তে সক্রিয় নেই। অনুগ্রহ করে আপনার API Key চেক করুন।"
        
        # Cache AI responses for identical queries for 1 hour
        cache_key = f"ai_advisor_response_{query.strip().lower()}"
        cached_response = cache_instance.get(cache_key)
        if cached_response:
            return cached_response

        context = AdvisorService.get_business_context(db)
        
        system_prompt = f"""
        তুমি একজন 'AI Merchant Advisor'। তোমার কাজ হলো ব্যবসায়ীদের তাদের দোকানের ডেটা বিশ্লেষণ করে পরামর্শ দেওয়া। 
        খুব মার্জিত এবং প্রফেশনাল বাংলায় উত্তর দাও।
        দোকানের ডেটা: {context}
        
        ব্যবসায়ীর প্রশ্ন: {query}
        
        পরামর্শ দেওয়ার সময় ডেটা সাপোর্ট ব্যবহার করো।
        """

        try:
            response = model.generate_content(system_prompt)
            answer = response.text
            cache_instance.set(cache_key, answer, ttl_seconds=3600) # 1 hour cache
            return answer
        except Exception as e:
            return f"ত্রুটি: {str(e)}"
