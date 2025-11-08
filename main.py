# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importando os routers corretos (arquivos admin_*)
from routers import (
    admin_products as products,
    admin_addons as addons,
    admin_categories as categories,
    admin_coupons as coupons,
    admin_loyalty as loyalty,
    admin_settings as settings,
    admin_orders as orders,
    admin_reports as reports,
    admin_auth as auth,
)

app = FastAPI(title="MeatBurger Backend")

# Configuração do CORS para permitir requisições do frontend
origins = [
    "http://localhost:5173",  # Vite local dev
    "http://localhost:3000",  # React dev server
    "https://meatburger.com.py",  # Frontend deploy Hostinger
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo os routers
app.include_router(auth.router, prefix="/admin/auth", tags=["auth"])
app.include_router(products.router, prefix="/admin/products", tags=["products"])
app.include_router(addons.router, prefix="/admin/addons", tags=["addons"])
app.include_router(categories.router, prefix="/admin/categories", tags=["categories"])
app.include_router(coupons.router, prefix="/admin/coupons", tags=["coupons"])
app.include_router(loyalty.router, prefix="/admin/loyalty", tags=["loyalty"])
app.include_router(settings.router, prefix="/admin/settings", tags=["settings"])
app.include_router(orders.router, prefix="/admin/orders", tags=["orders"])
app.include_router(reports.router, prefix="/admin/reports", tags=["reports"])

# Test route
@app.get("/")
def read_root():
    return {"message": "MeatBurger Backend is running"}
