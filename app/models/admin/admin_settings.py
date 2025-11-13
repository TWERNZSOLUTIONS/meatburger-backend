from sqlalchemy import Column, Integer, String, Boolean, Time, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)

    # Horário de funcionamento
    opening_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)

    # Dias de funcionamento (lista de strings: ["Mon", "Tue", ...])
    days_open = Column(JSON, default=list)

    # Status de funcionamento (Aberto/Fechado)
    open = Column(Boolean, default=True)

    # Mensagem de aviso quando fechado
    closed_message = Column(String, nullable=True)

    # Links de redes sociais
    instagram_link = Column(String, nullable=True)
    whatsapp_link = Column(String, nullable=True)

    # Datas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
