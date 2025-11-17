from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict

from .market import MarketRead


class ProductBase(BaseModel):
    name: str
    brand: str | None = None
    unit: str
    category: str
    description: str | None = None


class ProductRead(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MarketPriceRead(BaseModel):
    market: MarketRead
    price: float
    currency: str
    promo: bool
    stock_status: str
    last_updated: datetime
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProductStats(BaseModel):
    min_price: float
    max_price: float
    avg_price: float
    price_spread: float
    min_price_market: MarketRead
    max_price_market: MarketRead
    market_count: int


class ProductSearchResult(BaseModel):
    product: ProductRead
    prices: List[MarketPriceRead]
    stats: ProductStats


class HealthResponse(BaseModel):
    status: str
    message: str
