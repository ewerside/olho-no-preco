from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from ..models import Market


def list_markets(db: Session) -> List[Market]:
    return db.query(Market).order_by(Market.name).all()
