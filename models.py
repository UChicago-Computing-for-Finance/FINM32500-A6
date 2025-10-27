from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional

@dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float
    daily_volume: Optional[float] = None