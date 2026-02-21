import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from app.products.models import Product
from app.utils.cache import cache_instance

# Configure Gemini
try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception:
    model = None

class ChatbotService:
    @staticmethod
    def get_reply(db: Session, message: str, product_id: int = None):
        # Cache key based on message and product_id
        cache_key = f"chatbot_reply_{product_id}_{message.strip().lower()}"
        cached_reply = cache_instance.get(cache_key)
        if cached_reply:
            return cached_reply

        product_context = ""
        if product_id:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product:
                product_context = f"Name:{product.product_name}, Price:{product.price}, Info:{product.variant}"

        system_prompt = f"You are a helpful support agent. Reply in polite Bengali. Context: {product_context}. Input: {message}"

        if not model:
            return "দুঃখিত, বর্তমানে এআই সার্ভিসটি পাওয়া যাচ্ছে না।"

        try:
            response = model.generate_content(system_prompt)
            reply = response.text
            cache_instance.set(cache_key, reply, ttl_seconds=3600) # Cache for 1 hour
            return reply
        except Exception as e:
            return f"ত্রুটি: {str(e)}"
