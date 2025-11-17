from __future__ import annotations

from sqlalchemy.exc import SQLAlchemyError

from backend.app.data.sample_data import MARKETS, PRICE_ENTRIES, PRODUCTS
from backend.app.db.database import Base, engine, session_scope
from backend.app.models import Market, Product, ProductPrice


def reset_schema() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed_entities() -> None:
    with session_scope() as session:
        market_entities: dict[str, Market] = {}
        for data in MARKETS:
            market = Market(**data)
            session.add(market)
            market_entities[data["name"]] = market

        product_entities: dict[str, Product] = {}
        for data in PRODUCTS:
            product = Product(**data)
            session.add(product)
            product_entities[data["name"]] = product
        session.flush()

        for entry in PRICE_ENTRIES:
            product = product_entities[entry["product"]]
            market = market_entities[entry["market"]]
            price = ProductPrice(
                product_id=product.id,
                market_id=market.id,
                price=entry["price"],
                promo=entry["promo"],
                stock_status=entry["stock_status"],
                last_updated=entry["last_updated"],
                notes=entry["notes"],
            )
            session.add(price)


def main() -> None:
    try:
        reset_schema()
        seed_entities()
        print("Banco de dados inicializado com sucesso.")
    except SQLAlchemyError as exc:  # pragma: no cover - apenas CLI
        print(f"Erro ao popular o banco: {exc}")
        raise


if __name__ == "__main__":
    main()
