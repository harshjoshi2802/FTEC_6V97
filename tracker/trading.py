import logging
from decimal import Decimal

from .errors import InsufficientFundsError, InsufficientSharesError
from .models import Position, Trade
from .validation import number, share_quantity

logger = logging.getLogger(__name__)


class TradingService:
    def __init__(self, assets, portfolios):
        self.assets = assets
        self.portfolios = portfolios
        self.cash = Decimal("0")

    def deposit(self, amount):
        amount = number(amount, "Deposit")
        self.cash += amount
        logger.info("Deposited %s; cash %s", amount, self.cash)

    def buy(self, ticker, quantity, price):
        portfolio = self.portfolios.selected()
        asset = self.assets.get(ticker)
        quantity = share_quantity(quantity)
        price = number(price, "Buy price")
        cost = quantity * price
        if cost > self.cash:
            raise InsufficientFundsError("Not enough cash for this purchase.")
        position = portfolio.positions.get(asset.ticker, Position())
        new_quantity = position.quantity + quantity
        average_cost = (position.quantity * position.average_cost + cost) / new_quantity
        portfolio.positions[asset.ticker] = Position(new_quantity, average_cost)
        self.cash -= cost
        portfolio.trades.append(Trade("buy", asset.ticker, quantity, price))
        logger.info("Bought %s %s at %s in %s", quantity, asset.ticker, price, portfolio.name)

    def sell(self, ticker, quantity, price):
        portfolio = self.portfolios.selected()
        asset = self.assets.get(ticker)
        quantity = share_quantity(quantity)
        price = number(price, "Sell price", allow_zero=True)
        position = portfolio.positions.get(asset.ticker)
        if position is None or quantity > position.quantity:
            raise InsufficientSharesError("Not enough shares in the selected portfolio.")
        proceeds = quantity * price
        gain = (price - position.average_cost) * quantity
        self.cash += proceeds
        portfolio.realized_gain += gain
        position.quantity -= quantity
        if position.quantity == 0:
            del portfolio.positions[asset.ticker]
        portfolio.trades.append(Trade("sell", asset.ticker, quantity, price))
        logger.info("Sold %s %s at %s in %s; gain %s", quantity, asset.ticker, price, portfolio.name, gain)
