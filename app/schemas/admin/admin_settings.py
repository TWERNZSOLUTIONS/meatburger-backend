from pydantic import BaseModel, HttpUrl, ConfigDict, Field
from typing import List, Optional
from datetime import time, datetime

class SiteSettingsBase(BaseModel):
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None
    days_open: Optional[List[str]] = Field(default_factory=list)
    open: Optional[bool] = True
    closed_message: Optional[str] = None
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

    model_config = ConfigDict(from_attributes=True)
