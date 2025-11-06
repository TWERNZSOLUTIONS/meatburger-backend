# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routers.admin import router as admin_router
from app.routers.admin import admin_settings  # ✅ adicionado

app = FastAPI(
    title="Delivery Backend",
    description="API do backend do sistema de delivery",
    version="1.0.0"
)

# ----------------- CORS -----------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "https://meatburger.com.py",      # ✅ domínio da Hostinger
    "https://www.meatburger.com.py",  # ✅ versão com www
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ✅ domínios autorizados
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Rotas -----------------
app.include_router(admin_router, prefix="/admin")
app.include_router(admin_settings.router, prefix="/admin", tags=["Admin - Configurações"])

# ----------------- Uploads -----------------
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "API do Delivery rodando perfeitamente 🚀"}
