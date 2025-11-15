from pydantic import BaseModel, HttpUrl, Field, ConfigDict
from typing import Optional, Dict
from datetime import datetime

# Configuração de cada dia da semana
class DayConfig(BaseModel):
    enabled: bool
    open: str
    close: str

# Fechamento manual
class ManualClose(BaseModel):
    enabled: bool = False
    reason: str = ""

class SiteSettingsBase(BaseModel):
    days: Dict[str, DayConfig]
    manualClose: ManualClose

    open: Optional[int] = 1  # <- STATUS FINAL DA LOJA (adicionado)

    store_name: Optional[str] = None
    store_phone: Optional[str] = None
    store_address: Optional[str] = None

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
