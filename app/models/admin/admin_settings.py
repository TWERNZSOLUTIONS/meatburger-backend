from sqlalchemy import Column, Integer, String, Boolean, Time, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class SiteSettings(Base):
    __tablename__ = "site_settings"

    id = Column(Integer, primary_key=True, index=True)

    opening_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)
    days_open = Column(JSON, default=list)

    open = Column(Boolean, default=True)
    closed_message = Column(String, nullable=True)

    instagram_link = Column(String, nullable=True)
    whatsapp_link = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
