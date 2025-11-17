from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db.database import Base


class Market(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    neighborhood = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String(2), nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    opening_hours = Column(String, nullable=True)

    prices = relationship("ProductPrice", back_populates="market", cascade="all, delete-orphan")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Market {self.name} ({self.city}/{self.state})>"
