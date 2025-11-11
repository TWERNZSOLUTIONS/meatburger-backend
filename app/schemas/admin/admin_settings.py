# backend/app/schemas/admin/admin_setting.py
from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import time, datetime

# ----------------- Schemas de Configurações do Site -----------------
class SiteSettingsBase(BaseModel):
    """Schema base com campos comuns das configurações do site."""
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    working_days: Optional[List[str]] = []
    is_open: Optional[bool] = True
    notice_message: Optional[str] = None
    instagram_link: Optional[HttpUrl] = None
    whatsapp_link: Optional[HttpUrl] = None

class SiteSettingsCreate(SiteSettingsBase):
    """Schema para criação de novas configurações do site."""
    pass

class SiteSettingsUpdate(SiteSettingsBase):
    """Schema para atualização parcial das configurações do site."""
    pass

class SiteSettingsOut(SiteSettingsBase):
    """Schema de saída, incluindo id e timestamps."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # ✅ Compatível com Pydantic v2
