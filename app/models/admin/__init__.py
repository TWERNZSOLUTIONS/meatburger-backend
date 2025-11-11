# backend/app/models/__init__.py
# Apenas expõe as models principais para importação externa
from app.models.admin.admin_addon import Addon
from app.models.admin.admin_category import Category
from app.models.admin.admin_coupon import Coupon
from app.models.admin.admin_product import Product
from app.models.admin.admin_settings import SiteSettings
from app.models.admin.admin_order import AdminOrder
from app.models.admin.admin import Admin
from app.models.admin.admin_loyalty import Loyalty
from app.models.customer import Customer
