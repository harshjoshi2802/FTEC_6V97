import logging
from decimal import Decimal

from .errors import (DuplicateError, NotFoundError, NoPortfolioSelectedError,
                     PortfolioNotEmptyError)
from .models import Portfolio
from .validation import required_text

logger = logging.getLogger(__name__)


class PortfolioService:
    def __init__(self):
        self.portfolios = {}
        self.selected_name = None

    def get(self, name):
        name = required_text(name, "Portfolio name")
        try:
            return self.portfolios[name]
        except KeyError as error:
            raise NotFoundError(f"No portfolio named {name}.") from error

    def create(self, name, strategy):
        name = required_text(name, "Portfolio name")
        strategy = required_text(strategy, "Strategy")
        if name in self.portfolios:
            raise DuplicateError(f"Portfolio {name} already exists.")
        self.portfolios[name] = Portfolio(name, strategy)
        logger.info("Created portfolio %s", name)

    def select(self, name):
        self.selected_name = self.get(name).name
        logger.info("Selected portfolio %s", self.selected_name)

    def selected(self):
        if self.selected_name is None:
            raise NoPortfolioSelectedError("Select a portfolio before continuing.")
        return self.portfolios[self.selected_name]

    def delete(self, name):
        portfolio = self.get(name)
        if any(position.quantity > 0 for position in portfolio.positions.values()):
            raise PortfolioNotEmptyError("Sell all shares before deleting this portfolio.")
        del self.portfolios[portfolio.name]
        if self.selected_name == portfolio.name:
            self.selected_name = None
        logger.info("Deleted portfolio %s", portfolio.name)

    def list_portfolios(self):
        return [(p, p.name == self.selected_name) for p in self.portfolios.values()]

    def summary(self, assets):
        portfolio = self.selected()
        rows = []
        market_total = Decimal("0")
        unrealized_total = Decimal("0")
        complete = True
        for ticker, position in portfolio.positions.items():
            price = assets.prices.get(ticker)
            value = gain = None
            if price is None:
                complete = False
            else:
                value = price * position.quantity
                gain = (price - position.average_cost) * position.quantity
                market_total += value
                unrealized_total += gain
            rows.append((ticker, position.quantity, position.average_cost, price, value, gain))
        return portfolio.name, rows, market_total, unrealized_total, portfolio.realized_gain, complete
