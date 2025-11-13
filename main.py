from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import public
from app.routers.admin import (
    admin_auth,
    admin_categories,
    admin_products,
    admin_addons,
    admin_orders,
    admin_coupons,
    admin_loyalty,
    admin_loyalty_config,
    admin_reports,
    admin_settings
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Delivery Backend", version="1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas públicas
app.include_router(public.router, prefix="/api")

# Rotas admin
app.include_router(admin_auth.router, prefix="/apiAdmin/auth", tags=["Admin Auth"])
app.include_router(admin_categories.router, prefix="/apiAdmin/categories", tags=["Admin Categories"])
app.include_router(admin_products.router, prefix="/apiAdmin/products", tags=["Admin Products"])
app.include_router(admin_addons.router, prefix="/apiAdmin/addons", tags=["Admin Addons"])
app.include_router(admin_orders.router, prefix="/apiAdmin/orders", tags=["Admin Orders"])
app.include_router(admin_coupons.router, prefix="/apiAdmin/coupons", tags=["Admin Coupons"])
app.include_router(admin_loyalty.router, prefix="/apiAdmin/loyalty", tags=["Admin Loyalty"])
app.include_router(admin_loyalty_config.router, prefix="/apiAdmin/loyalty-config", tags=["Admin Loyalty Config"])
app.include_router(admin_reports.router, prefix="/apiAdmin/reports", tags=["Admin Reports"])
app.include_router(admin_settings.router, prefix="/apiAdmin/settings", tags=["Admin Settings"])
