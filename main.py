# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 🔹 Importa suas rotas
from routers import products, addons, categories, coupons, loyalty, settings, orders, reports, auth

app = FastAPI(
    title="MeatBurger Backend",
    description="API para o painel administrativo e app de delivery",
    version="1.0.0",
)

# 🔹 Configuração CORS
origins = [
    "https://meatburger.com.py",  # Frontend Hostinger
    "http://localhost:5173",      # Desenvolvimento local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Inclui os routers
app.include_router(auth.router, prefix="/admin/auth", tags=["Auth"])
app.include_router(products.router, prefix="/admin/products", tags=["Products"])
app.include_router(addons.router, prefix="/admin/addons", tags=["Addons"])
app.include_router(categories.router, prefix="/admin/categories", tags=["Categories"])
app.include_router(coupons.router, prefix="/admin/coupons", tags=["Coupons"])
app.include_router(loyalty.router, prefix="/admin/loyalty", tags=["Loyalty"])
app.include_router(settings.router, prefix="/admin/settings", tags=["Settings"])
app.include_router(orders.router, prefix="/admin/orders", tags=["Orders"])
app.include_router(reports.router, prefix="/admin/reports", tags=["Reports"])

# 🔹 Rota de teste
@app.get("/ping")
async def ping():
    return {"message": "pong"}
