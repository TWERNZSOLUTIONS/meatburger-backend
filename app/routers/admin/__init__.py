from fastapi import APIRouter

router = APIRouter()

from . import (
    admin_auth,
    admin_categories,
    admin_products,
    admin_addons,
    admin_orders,
    admin_coupons,
    admin_loyalty,
    admin_loyalty_config,
    admin_reports,
    admin_settings,
)

# AUTH
router.include_router(admin_auth.router, prefix="/auth", tags=["Admin Auth"])

# CATEGORIES
router.include_router(admin_categories.router, prefix="/categories", tags=["Admin Categories"])

# PRODUCTS
router.include_router(admin_products.router, prefix="/products", tags=["Admin Products"])

# ADDONS
router.include_router(admin_addons.router, prefix="/addons", tags=["Admin Addons"])

# ORDERS
router.include_router(admin_orders.router, prefix="/orders", tags=["Admin Orders"])

# COUPONS
router.include_router(admin_coupons.router, prefix="/coupons", tags=["Admin Coupons"])

# LOYALTY
router.include_router(admin_loyalty.router, prefix="/loyalty", tags=["Admin Loyalty"])
router.include_router(admin_loyalty_config.router, prefix="/loyalty-config", tags=["Admin Loyalty Config"])

# REPORTS
router.include_router(admin_reports.router, prefix="/reports", tags=["Admin Reports"])

# SETTINGS
router.include_router(admin_settings.router, prefix="/settings", tags=["Admin Settings"])
