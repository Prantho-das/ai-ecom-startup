import google.generativeai as genai
import os
from sqlalchemy.orm import Session
from app.products.models import ProductReview

class SentimentService:
    @staticmethod
    def analyze_reviews(db: Session, product_id: int):
        reviews = db.query(ProductReview).filter(ProductReview.product_id == product_id).all()
        if not reviews:
            return "এই পণ্যের কোনো রিভিউ পাওয়া যায়নি।"
            
        combined_text = " ".join([r.review_text for r in reviews])
        
        # Use Gemini for sentiment summarization
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            তুমি একজন কাস্টমার ফিডব্যাক এনালিস্ট। নিচের রিভিউগুলো বিশ্লেষণ করে ব্যবসায়ীকে বাংলায় একটি সামারি দাও।
            রিভিউসমূহ: {combined_text}
            
            আউটপুট ফরম্যাট:
            ১. সামগ্রিক সেন্টিমেন্ট (Positive/Negative/Neutral)
            ২. কাস্টমারদের প্রধান অভিযোগ বা প্রশংসা
            ৩. ব্যবসায়ীর জন্য প্রয়োজনীয় পদক্ষেপ।
            """
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"সেন্টিমেন্ট বিশ্লেষণে ত্রুটি: {str(e)}"
