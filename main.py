# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# routers admin (imports iguais aos seus)
from app.routers.admin import (
    admin_auth,
    admin_products,
    admin_addons,
    admin_categories,
    admin_coupons,
    admin_loyalty,
    admin_settings,
    admin_reports,
    admin_orders,
)

app = FastAPI(
    title="Delivery Backend",
    description="API do backend do sistema de delivery",
    version="1.0.0"
)

# CORS: permitir domínios de produção e desenvolvimento local
origins = [
    "https://meatburger.com.py",
    "https://www.meatburger.com.py",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Inclui routers principais ===
# Mantém os prefixes /admin/... (prod) e adiciona aliases sem /admin para compatibilidade
# Admin auth: disponível em /admin/auth/* e também em /admin/* (ex: /admin/login)
app.include_router(admin_auth.router, prefix="/admin/auth", tags=["Admin Auth"])
app.include_router(admin_auth.router, prefix="/admin", tags=["Admin Auth (alias)"])

# Produtos (disponível em /admin/products e também em /products)
app.include_router(admin_products.router, prefix="/admin/products", tags=["Admin Products"])
app.include_router(admin_products.router, prefix="/products", tags=["Products (alias)"])

# Addons (disponível em /admin/addons e também em /addons)
app.include_router(admin_addons.router, prefix="/admin/addons", tags=["Admin Addons"])
app.include_router(admin_addons.router, prefix="/addons", tags=["Addons (alias)"])

# Categories (disponível em /admin/categories e também em /categories)
app.include_router(admin_categories.router, prefix="/admin/categories", tags=["Admin Categories"])
app.include_router(admin_categories.router, prefix="/categories", tags=["Categories (alias)"])

# Coupons, Loyalty, Settings, Reports, Orders — mesmos prefixes duplos
app.include_router(admin_coupons.router, prefix="/admin/coupons", tags=["Admin Coupons"])
app.include_router(admin_coupons.router, prefix="/coupons", tags=["Coupons (alias)"])

app.include_router(admin_loyalty.router, prefix="/admin/loyalty", tags=["Admin Loyalty"])
app.include_router(admin_loyalty.router, prefix="/loyalty", tags=["Loyalty (alias)"])

app.include_router(admin_settings.router, prefix="/admin/settings", tags=["Admin Settings"])
app.include_router(admin_settings.router, prefix="/settings", tags=["Settings (alias)"])

app.include_router(admin_reports.router, prefix="/admin/reports", tags=["Admin Reports"])
app.include_router(admin_reports.router, prefix="/reports", tags=["Reports (alias)"])

app.include_router(admin_orders.router, prefix="/admin/orders", tags=["Admin Orders"])
app.include_router(admin_orders.router, prefix="/orders", tags=["Orders (alias)"])

# Serve uploads (permite acesso a imagens em /uploads)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "🚀 API do Delivery rodando perfeitamente no Render!"}
