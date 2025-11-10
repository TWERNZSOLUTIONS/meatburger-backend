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
    "http://localhost:3000",  # útil para testes locais
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Rotas administrativas -----------------
# ✅ Agora cada router já define seu prefixo internamente (ex: /admin/products)
app.include_router(admin_auth.router)
app.include_router(admin_products.router)
app.include_router(admin_categories.router)
app.include_router(admin_addons.router)
app.include_router(admin_coupons.router)
app.include_router(admin_loyalty.router)
app.include_router(admin_orders.router)
app.include_router(admin_reports.router)
app.include_router(admin_settings.router)

# ----------------- Uploads -----------------
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ----------------- Rota raiz -----------------
@app.get("/")
def read_root():
    return {"message": "API do Delivery rodando perfeitamente 🚀"}
