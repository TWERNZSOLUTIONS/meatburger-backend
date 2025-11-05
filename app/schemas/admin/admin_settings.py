from pydantic import BaseModel, HttpUrl, ConfigDict
from typing import List, Optional
from datetime import time, datetime

class SiteSettingsBase(BaseModel):
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    working_days: Optional[List[str]] = []
    is_open: Optional[bool] = True
    notice_message: Optional[str] = None
    instagram_link: Optional[HttpUrl] = None
    whatsapp_link: Optional[HttpUrl] = None


class SiteSettingsCreate(SiteSettingsBase):
    pass


class SiteSettingsUpdate(SiteSettingsBase):
    pass


class SiteSettingsOut(SiteSettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)  # ✅ substitui orm_mode no Pydantic v2
