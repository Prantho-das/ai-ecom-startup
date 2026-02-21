from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List
import os

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "test@example.com"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "password"),
    MAIL_FROM = os.getenv("MAIL_FROM", "admin@ecompredictor.com"),
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

class NotificationService:
    @staticmethod
    async def send_email(subject: str, recipients: List[str], body: str):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype="html"
        )
        fm = FastMail(conf)
        try:
            await fm.send_message(message)
            return True
        except Exception:
            return False

    @staticmethod
    async def stock_alert_notification(product_name: str, stock_level: int, merchant_email: str):
        subject = f"⚠️ স্টক অ্যালার্ট: {product_name} শেষ হয়ে যাচ্ছে!"
        body = f"""
        <html>
            <body>
                <h3>আসসালামু আলাইকুম,</h3>
                <p>আপনার দোকানের <b>{product_name}</b> পণ্যটির স্টক বর্তমানে <b>{stock_level}</b> পিস।</p>
                <p>এআই প্রেডিকশন অনুযায়ী এটি আগামী ৩ দিনের মধ্যে শেষ হয়ে যেতে পারে। অনুগ্রহ করে এখনই সোর্সিং করুন।</p>
                <br>
                <p>ধন্যবাদ,<br>EcomPredictor AI</p>
            </body>
        </html>
        """
        await NotificationService.send_email(subject, [merchant_email], body)
