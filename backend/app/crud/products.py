from __future__ import annotations

from typing import List, Optional, TypedDict

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from ..models import Product, ProductPrice
from ..services.analytics import PriceStats, build_price_stats


class ProductSearchPayload(TypedDict):
    product: Product
    prices: List[ProductPrice]
    stats: PriceStats


def search_products(db: Session, query: Optional[str] = None) -> List[ProductSearchPayload]:
    product_query = db.query(Product)
    if query:
        normalized = f"%{query.lower()}%"
        product_query = product_query.filter(func.lower(Product.name).like(normalized))

    products = (
        product_query.options(joinedload(Product.prices).joinedload(ProductPrice.market))
        .order_by(Product.category, Product.name)
        .all()
    )

    payload: List[ProductSearchPayload] = []
    for product in products:
        prices = [price for price in product.prices if price.market is not None]
        if not prices:
            continue
        stats = build_price_stats(prices)
        payload.append({"product": product, "prices": prices, "stats": stats})

    return payload


def get_product(db: Session, product_id: int) -> Optional[ProductSearchPayload]:
    product = (
        db.query(Product)
        .options(joinedload(Product.prices).joinedload(ProductPrice.market))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        return None

    prices = [price for price in product.prices if price.market is not None]
    if not prices:
        return None

    stats = build_price_stats(prices)
    return {"product": product, "prices": prices, "stats": stats}
