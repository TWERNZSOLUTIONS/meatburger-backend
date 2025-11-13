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

# AUTENTICAÇÃO
router.include_router(admin_auth.router, prefix="/admin/auth", tags=["Admin Auth"])

# CATEGORIAS
router.include_router(admin_categories.router, prefix="/admin/categories", tags=["Admin Categories"])

# PRODUTOS
router.include_router(admin_products.router, prefix="/admin/products", tags=["Admin Products"])

# ADICIONAIS
router.include_router(admin_addons.router, prefix="/admin/addons", tags=["Admin Addons"])

# PEDIDOS
router.include_router(admin_orders.router, prefix="/admin/orders", tags=["Admin Orders"])

# CUPONS
router.include_router(admin_coupons.router, prefix="/admin/coupons", tags=["Admin Coupons"])

# FIDELIDADE
router.include_router(admin_loyalty.router, prefix="/admin/loyalty", tags=["Admin Loyalty"])
router.include_router(admin_loyalty_config.router, prefix="/admin/loyalty-config", tags=["Admin Loyalty Config"])

# RELATÓRIOS
router.include_router(admin_reports.router, prefix="/admin/reports", tags=["Admin Reports"])

# CONFIGURAÇÕES
router.include_router(admin_settings.router, prefix="/admin/settings", tags=["Admin Settings"])
