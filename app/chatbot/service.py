import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from app.products.models import Product
from app.config import settings

# Configure Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = None

class ChatbotService:
    @staticmethod
    def get_reply(db: Session, message: str, product_id: int = None):
        product_context = ""
        if product_id:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                product_context = f"""
                পণ্যটির নাম: {product.product_name}
                দাম: {product.price} টাকা
                বিস্তারিত: {product.variant or 'তথ্য নেই'}
                ওয়েবসাইট: {product.source_website}
                """

        system_prompt = f"""
        তুমি একজন দক্ষ কাস্টমার সাপোর্ট এজেন্ট। তোমার কাজ হলো কাস্টমারদের প্রশ্নের উত্তর দেওয়া। 
        সব উত্তর মার্জিত এবং বন্ধুসুলভ বাংলায় দাও। 
        যদি পণ্যের তথ্য দেওয়া থাকে, তবে সেটি ব্যবহার করো।
        পণ্যের তথ্য:
        {product_context}
        
        কাস্টমারের প্রশ্ন: {message}
        """

        if not model:
            return "দুঃখিত, বর্তমানে এআই সার্ভিসটি পাওয়া যাচ্ছে না। অনুগ্রহ করে পরে চেষ্টা করুন।"

        try:
            response = model.generate_content(system_prompt)
            return response.text
        except Exception as e:
            return f"ত্রুটি: {str(e)}"
