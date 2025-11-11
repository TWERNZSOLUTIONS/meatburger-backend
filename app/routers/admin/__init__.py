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
    admin_reports,
    admin_settings
)

router.include_router(admin_auth.router, prefix="/auth", tags=["Admin Auth"])
router.include_router(admin_categories.router, prefix="/categories", tags=["Admin Categories"])
router.include_router(admin_products.router, prefix="/products", tags=["Admin Products"])
router.include_router(admin_addons.router, prefix="/addons", tags=["Admin Addons"])
router.include_router(admin_orders.router, prefix="/orders", tags=["Admin Orders"])
router.include_router(admin_coupons.router, prefix="/coupons", tags=["Admin Coupons"])
router.include_router(admin_loyalty.router, prefix="/loyalty", tags=["Admin Loyalty"])
router.include_router(admin_reports.router, prefix="/reports", tags=["Admin Reports"])
router.include_router(admin_settings.router, prefix="/settings", tags=["Admin Settings"])
