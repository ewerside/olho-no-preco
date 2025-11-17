from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .market import MarketUpsert
from .product import ProductUpsert


class PricePayload(BaseModel):
    price: float
    currency: str | None = "BRL"
    promo: bool = False
    stock_status: str | None = None
    notes: str | None = None
    last_updated: datetime | None = None


class EntryCreate(BaseModel):
    product: ProductUpsert
    market: MarketUpsert
    price: PricePayload

    model_config = ConfigDict(str_strip_whitespace=True)
