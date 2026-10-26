from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Asset:
    ticker: str
    name: str


@dataclass
class Position:
    quantity: int = 0
    average_cost: Decimal = Decimal("0")


@dataclass
class Trade:
    side: str
    ticker: str
    quantity: int
    price: Decimal


@dataclass
class Portfolio:
    name: str
    strategy: str
    positions: dict = field(default_factory=dict)
    trades: list = field(default_factory=list)
    realized_gain: Decimal = Decimal("0")
