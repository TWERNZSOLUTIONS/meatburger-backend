from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)

    # Dias e horários da semana
    days = Column(JSON, default={
        "monday":    {"enabled": True, "open": "18:00", "close": "23:00"},
        "tuesday":   {"enabled": True, "open": "18:00", "close": "23:00"},
        "wednesday": {"enabled": True, "open": "18:00", "close": "23:00"},
        "thursday":  {"enabled": True, "open": "18:00", "close": "23:00"},
        "friday":    {"enabled": True, "open": "18:00", "close": "02:00"},
        "saturday":  {"enabled": True, "open": "18:00", "close": "02:00"},
        "sunday":    {"enabled": True, "open": "18:00", "close": "23:00"}
    })

    # Fechamento manual pelo administrador
    manualClose = Column(JSON, default={
        "enabled": False,
        "reason": ""
    })

    # Status calculado da loja (1 = aberta / 0 = fechada)
    open = Column(Integer, default=1)

    # Informações gerais da loja
    store_name = Column(String, nullable=True)
    store_phone = Column(String, nullable=True)
    store_address = Column(String, nullable=True)

    instagram_link = Column(String, nullable=True)
    whatsapp_link = Column(String, nullable=True)

    # Datas de criação e atualização
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
