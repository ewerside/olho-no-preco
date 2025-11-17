from pydantic import BaseModel, ConfigDict


class MarketBase(BaseModel):
    name: str
    neighborhood: str
    city: str
    state: str
    address: str
    phone: str | None = None
    opening_hours: str | None = None


class MarketRead(MarketBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
