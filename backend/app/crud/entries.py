from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models import Market, Product, ProductPrice
from ..schemas.entry import EntryCreate
from . import markets as market_crud
from . import products as product_crud


def _default_text(value: str | None, fallback: str) -> str:
    if value and value.strip():
        return value.strip()
    return fallback


def _upsert_product(db: Session, payload: EntryCreate) -> Product:
    data = payload.product
    product = product_crud.get_product_by_name(db, data.name)
    if product:
        for field in ("brand", "unit", "category", "description"):
            incoming = getattr(data, field)
            if incoming:
                setattr(product, field, incoming)
        db.flush()
        return product

    product = Product(
        name=data.name.strip(),
        brand=_default_text(data.brand, "Not informed"),
        unit=_default_text(data.unit, "unit"),
        category=_default_text(data.category, "General"),
        description=_default_text(data.description, "Added via dashboard"),
    )
    db.add(product)
    db.flush()
    return product


def _upsert_market(db: Session, payload: EntryCreate) -> Market:
    data = payload.market
    market = market_crud.get_market_by_name(db, data.name)
    if market:
        for field in ("neighborhood", "city", "state", "address", "phone", "opening_hours"):
            incoming = getattr(data, field)
            if incoming:
                setattr(market, field, incoming)
        db.flush()
        return market

    market = Market(
        name=data.name.strip(),
        neighborhood=_default_text(data.neighborhood, "Unknown"),
        city=_default_text(data.city, "Rio de Janeiro"),
        state=_default_text(data.state, "RJ"),
        address=_default_text(data.address, "Not informed"),
        phone=data.phone,
        opening_hours=data.opening_hours,
    )
    db.add(market)
    db.flush()
    return market


def create_entry(db: Session, payload: EntryCreate):
    product = _upsert_product(db, payload)
    market = _upsert_market(db, payload)
    price_data = payload.price

    price = ProductPrice(
        product_id=product.id,
        market_id=market.id,
        price=price_data.price,
        currency=price_data.currency or "BRL",
        promo=price_data.promo,
        stock_status=_default_text(price_data.stock_status, "Available"),
        notes=price_data.notes,
        last_updated=price_data.last_updated or datetime.now(timezone.utc),
    )
    db.add(price)
    db.commit()

    return product_crud.get_product(db, product.id)
