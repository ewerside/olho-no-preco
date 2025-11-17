from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    brand = Column(String, nullable=True)
    unit = Column(String, nullable=False, default="unidade")
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)

    prices = relationship("ProductPrice", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Product {self.name} ({self.brand})>"
