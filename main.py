# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Importando routers do admin
from app.routers.admin import (
    admin_auth,
    admin_products,
    admin_categories,
    admin_addons,
    admin_coupons,
    admin_loyalty,
    admin_orders,
    admin_reports,
    admin_settings,
)

app = FastAPI(
    title="Delivery Backend",
    description="API do backend do sistema de delivery",
    version="1.0.0"
)

# ----------------- CORS -----------------
origins = [
    "https://meatburger.com.py",
    "https://www.meatburger.com.py",
    "http://localhost:3000",  # para testes locais
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Rotas administrativas -----------------
# Aqui definimos apenas os prefixos principais
# Os arquivos internos (como admin_auth) NÃO devem repetir prefixos

app.include_router(admin_auth.router, prefix="/admin/auth", tags=["Admin Auth"])
app.include_router(admin_products.router, prefix="/admin/products", tags=["Admin Products"])
app.include_router(admin_categories.router, prefix="/admin/categories", tags=["Admin Categories"])
app.include_router(admin_addons.router, prefix="/admin/addons", tags=["Admin Addons"])
app.include_router(admin_coupons.router, prefix="/admin/coupons", tags=["Admin Coupons"])
app.include_router(admin_loyalty.router, prefix="/admin/loyalty", tags=["Admin Loyalty"])
app.include_router(admin_orders.router, prefix="/admin/orders", tags=["Admin Orders"])
app.include_router(admin_reports.router, prefix="/admin/reports", tags=["Admin Reports"])
app.include_router(admin_settings.router, prefix="/admin/settings", tags=["Admin Settings"])

# ----------------- Uploads -----------------
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ----------------- Rota raiz -----------------
@app.get("/")
def read_root():
    return {"message": "🚀 API do Delivery rodando perfeitamente!"}
