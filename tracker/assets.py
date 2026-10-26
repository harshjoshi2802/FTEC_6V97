import logging

from .errors import DuplicateError, NotFoundError
from .models import Asset
from .validation import number, required_text

logger = logging.getLogger(__name__)


class AssetService:
    def __init__(self):
        self.assets = {}
        self.prices = {}

    def get(self, ticker):
        ticker = required_text(ticker, "Ticker").upper()
        try:
            return self.assets[ticker]
        except KeyError as error:
            raise NotFoundError(f"No asset with ticker {ticker}.") from error

    def add(self, ticker, name):
        ticker = required_text(ticker, "Ticker").upper()
        name = required_text(name, "Asset name")
        if ticker in self.assets:
            raise DuplicateError(f"Asset {ticker} already exists.")
        self.assets[ticker] = Asset(ticker, name)
        logger.info("Added asset %s", ticker)

    def set_price(self, ticker, price):
        asset = self.get(ticker)
        price = number(price, "Current price", allow_zero=True)
        self.prices[asset.ticker] = price
        logger.info("Set current price for %s to %s", asset.ticker, price)

    def list_assets(self):
        return [(asset, self.prices.get(asset.ticker)) for asset in self.assets.values()]
