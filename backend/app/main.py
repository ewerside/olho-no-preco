from __future__ import annotations

from typing import List, Sequence

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .core.config import get_settings
from .crud import markets as market_crud
from .crud import products as product_crud
from .db.database import Base, engine, get_db
from .models import ProductPrice
from .schemas import (
    HealthResponse,
    MarketPriceRead,
    MarketRead,
    ProductRead,
    ProductSearchResult,
    ProductStats,
)
from .services.analytics import PriceStats

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.project_name, version=settings.api_version)

allowed_origins = {settings.frontend_origin, "http://localhost:5173", "http://127.0.0.1:5173"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(allowed_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _serialize_stats(stats: PriceStats, prices: Sequence[ProductPrice]) -> ProductStats:
    return ProductStats(
        min_price=stats.min_entry.price,
        max_price=stats.max_entry.price,
        avg_price=stats.average,
        price_spread=stats.spread,
        min_price_market=MarketRead.from_orm(stats.min_entry.market),
        max_price_market=MarketRead.from_orm(stats.max_entry.market),
        market_count=len(prices),
    )


def _serialize_payload(payload: product_crud.ProductSearchPayload) -> ProductSearchResult:
    product_schema = ProductRead.from_orm(payload["product"])
    price_schema = [
        MarketPriceRead(
            market=MarketRead.from_orm(price.market),
            price=price.price,
            currency=price.currency,
            promo=price.promo,
            stock_status=price.stock_status,
            last_updated=price.last_updated,
            notes=price.notes,
        )
        for price in payload["prices"]
    ]
    stats_schema = _serialize_stats(payload["stats"], payload["prices"])
    return ProductSearchResult(product=product_schema, prices=price_schema, stats=stats_schema)


@app.get("/health", response_model=HealthResponse)
def healthcheck() -> HealthResponse:
    return HealthResponse(status="ok", message="API operacional")


@app.get("/products/search", response_model=List[ProductSearchResult])
def search_products(
    query: str | None = Query(None, description="Nome do produto para busca"),
    db: Session = Depends(get_db),
) -> List[ProductSearchResult]:
    payloads = product_crud.search_products(db, query)
    return [_serialize_payload(payload) for payload in payloads]


@app.get("/products/{product_id}", response_model=ProductSearchResult)
def get_product_detail(product_id: int, db: Session = Depends(get_db)) -> ProductSearchResult:
    payload = product_crud.get_product(db, product_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return _serialize_payload(payload)


@app.get("/markets", response_model=List[MarketRead])
def list_markets(db: Session = Depends(get_db)) -> List[MarketRead]:
    markets = market_crud.list_markets(db)
    return [MarketRead.from_orm(market) for market in markets]
