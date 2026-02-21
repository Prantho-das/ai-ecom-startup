from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as auth_router
from app.users.router import router as user_router
from app.products.router import router as product_router
from app.orders.router import router as order_router
from app.insights.router import router as insights_router
from app.chatbot.router import router as chatbot_router
from app.inventory.router import router as inventory_router
from app.advisor.router import router as advisor_router
from app.ui_router import router as ui_router
from app.admin_router import router as admin_router

import app.auth.models  # noqa: F401
import app.users.models  # noqa: F401
import app.products.models  # noqa: F401
import app.orders.models  # noqa: F401

app = FastAPI(
    title="E-Commerce Predictor API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(product_router, prefix="/api/v1/products", tags=["Products"])
app.include_router(order_router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(insights_router, prefix="/api/v1/insights", tags=["AI Insights"])
app.include_router(chatbot_router, prefix="/api/v1/chatbot", tags=["AI Chatbot"])
app.include_router(inventory_router, prefix="/api/v1/inventory", tags=["Inventory Intelligence"])
app.include_router(advisor_router, prefix="/api/v1/advisor", tags=["AI Merchant Advisor"])
app.include_router(ui_router)
app.include_router(admin_router, prefix="/api/v1")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "E-Commerce Predictor API"}
