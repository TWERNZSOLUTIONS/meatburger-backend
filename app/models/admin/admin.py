# backend/app/models/admin/admin.py
from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(180), unique=True, nullable=False)
    email = Column(String(300), unique=True, nullable=False)
    password = Column(String(285), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        return f"<Admin(username={self.username}, email={self.email})>"
