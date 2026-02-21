import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.orders.models import Order, OrderDetail
from app.products.models import Product
from app.users.models import User, UserAddress
from datetime import datetime, timedelta

# Configure Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = None

class AdvisorService:
    @staticmethod
    def get_business_context(db: Session):
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
         .limit(5).all()
        
        # Product stats
        top_products = db.query(
            Product.product_name,
            func.sum(OrderDetail.quantity).label('qty_sold')
        ).join(OrderDetail, Product.id == OrderDetail.product_id)\
         .group_by(Product.id)\
         .order_by(desc('qty_sold'))\
         .limit(5).all()

        context = f"""
        দোকানের মোট অর্ডার: {total_orders}
        মোট আয়: {total_revenue} টাকা
        
        বেশি বিক্রি হওয়া অঞ্চলসমূহ:
        {", ".join([f"{r[0]} ({r[1]} অর্ডার, {r[2]} টাকা)" for r in region_stats])}
        
        সেরা পণ্যসমূহ:
        {", ".join([f"{p[0]} ({p[1]} পিস)" for p in top_products])}
        """
        return context

    @staticmethod
    def ask_advisor(db: Session, query: str):
        if not model:
            return "দুঃখিত, এআই অ্যাডভাইজার এই মুহূর্তে সক্রিয় নেই। অনুগ্রহ করে আপনার API Key চেক করুন।"
        
        context = AdvisorService.get_business_context(db)
        
        system_prompt = f"""
        তুমি একজন 'AI Merchant Advisor'। তোমার কাজ হলো ব্যবসায়ীদের তাদের দোকানের ডেটা বিশ্লেষণ করে পরামর্শ দেওয়া। 
        খুব মার্জিত এবং প্রফেশনাল বাংলায় উত্তর দাও।
        নিচে দোকানের বর্তমান ডাটাবেজ থেকে কিছু তথ্য দেওয়া হলো। এই তথ্যের ভিত্তিতে উত্তর দাও:
        {context}
        
        ব্যবসায়ীর প্রশ্ন: {query}
        
        পরামর্শ দেওয়ার সময় ডেটা সাপোর্ট ব্যবহার করো (যেমন: 'রংপুর অঞ্চলে আপনার বিক্রি ভালো হচ্ছে, সেখানে বেশি ফোকাস করুন')।
        """

        try:
            response = model.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"ত্রুটি: {str(e)}"
