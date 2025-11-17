from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from ..db.database import Base


class ProductPrice(Base):
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    market_id = Column(Integer, ForeignKey("markets.id"), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="BRL")
    promo = Column(Boolean, default=False)
    stock_status = Column(String, default="Disponível")
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    notes = Column(String, nullable=True)

    product = relationship("Product", back_populates="prices")
    market = relationship("Market", back_populates="prices")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<ProductPrice product={self.product_id} market={self.market_id} price={self.price}>"
