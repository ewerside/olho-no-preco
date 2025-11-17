from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Sequence

from ..models import ProductPrice


@dataclass
class PriceStats:
    min_entry: ProductPrice
    max_entry: ProductPrice
    average: float
    spread: float


def build_price_stats(prices: Sequence[ProductPrice]) -> PriceStats:
    if not prices:
        raise ValueError("É necessário fornecer pelo menos um preço para calcular estatísticas.")

    ordered = sorted(prices, key=lambda item: item.price)
    min_entry = ordered[0]
    max_entry = ordered[-1]
    values = [item.price for item in prices]
    avg = round(mean(values), 2)
    spread = round(max_entry.price - min_entry.price, 2)
    return PriceStats(min_entry=min_entry, max_entry=max_entry, average=avg, spread=spread)
