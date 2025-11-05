from sqlalchemy import Column, Integer, String, Boolean, Time, JSON, DateTime
from app.database import Base
from datetime import datetime

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)

    # Horário de funcionamento
    open_time = Column(Time, nullable=True)
    close_time = Column(Time, nullable=True)

    # Dias de funcionamento (lista de strings: ["Segunda", "Terça", ...])
    working_days = Column(JSON, default=list)

    # Status de funcionamento (Aberto/Fechado)
    is_open = Column(Boolean, default=True)

    # Mensagem de aviso
    notice_message = Column(String, nullable=True)

    # Links de redes sociais
    instagram_link = Column(String, nullable=True)
    whatsapp_link = Column(String, nullable=True)

    # Datas
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
