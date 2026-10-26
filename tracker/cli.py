import logging

from .assets import AssetService
from .errors import InvalidInputError, TrackerError
from .portfolios import PortfolioService
from .trading import TradingService

logger = logging.getLogger(__name__)


def money(value):
    return "Not priced" if value is None else f"${value:,.2f}"


class Menu:
    def __init__(self):
        self.assets = AssetService()
        self.portfolios = PortfolioService()
        self.trading = TradingService(self.assets, self.portfolios)

    def add_asset(self):
        ticker = input("Ticker: ")
        name = input("Asset name: ")
        self.assets.add(ticker, name)
        print("Asset added.")

    def view_assets(self):
        assets = self.assets.list_assets()
        if not assets:
            print("No assets yet.")
        for asset, price in assets:
            print(f"{asset.ticker} | {asset.name} | {money(price)}")

    def set_price(self):
        ticker = input("Ticker: ")
        price = input("Current price: ")
        self.assets.set_price(ticker, price)
        print("Price updated.")

    def create_portfolio(self):
        name = input("Portfolio name: ")
        strategy = input("Investment strategy: ")
        self.portfolios.create(name, strategy)
        print("Portfolio created. Select it before trading.")

    def view_portfolios(self):
        portfolios = self.portfolios.list_portfolios()
        if not portfolios:
            print("No portfolios yet.")
        for portfolio, selected in portfolios:
            marker = " [selected]" if selected else ""
            print(f"{portfolio.name}{marker} | {portfolio.strategy}")

    def select_portfolio(self):
        self.portfolios.select(input("Portfolio name: "))
        print("Portfolio selected.")

    def delete_portfolio(self):
        self.portfolios.delete(input("Portfolio name: "))
        print("Portfolio deleted.")

    def view_selected(self):
        name, rows, value, gain, realized, complete = self.portfolios.summary(self.assets)
        print(f"Portfolio: {name}")
        print("Ticker | Shares | Average cost | Current price | Market value | Unrealized gain/loss")
        for ticker, quantity, average, price, market_value, unrealized in rows:
            print(f"{ticker} | {quantity} | {money(average)} | {money(price)} | {money(market_value)} | {money(unrealized)}")
        if not rows:
            print("No shares held.")
        label = "Total" if complete else "Priced holdings only (incomplete total)"
        print(f"{label} market value: {money(value)}")
        print(f"{label} unrealized gain/loss: {money(gain)}")
        print(f"Realized gain/loss: {money(realized)}")

    def deposit(self):
        self.trading.deposit(input("Amount to deposit: "))
        self.view_cash()

    def view_cash(self):
        print(f"Cash balance: {money(self.trading.cash)}")

    def trade(self, action):
        ticker = input("Ticker: ")
        quantity = input("Number of shares: ")
        price = input("Price per share: ")
        action(ticker, quantity, price)
        print("Trade completed.")
        self.view_cash()

    def run(self):
        print("Welcome to Portfolio Tracker!")
        actions = {
            "1": ("Add asset", self.add_asset),
            "2": ("View assets", self.view_assets),
            "3": ("Set current price", self.set_price),
            "4": ("Create portfolio", self.create_portfolio),
            "5": ("View portfolios", self.view_portfolios),
            "6": ("Select portfolio", self.select_portfolio),
            "7": ("Delete portfolio", self.delete_portfolio),
            "8": ("View selected portfolio", self.view_selected),
            "9": ("Deposit funds", self.deposit),
            "10": ("View cash balance", self.view_cash),
            "11": ("Buy shares", lambda: self.trade(self.trading.buy)),
            "12": ("Sell shares", lambda: self.trade(self.trading.sell)),
        }
        while True:
            print("\nMain menu")
            for key, (label, _) in actions.items():
                print(f"{key}. {label}")
            print("0. Quit")
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye!")
                return
            try:
                if choice not in actions:
                    raise InvalidInputError("Choose a menu option from 0 to 12.")
                actions[choice][1]()
            except TrackerError as error:
                logger.warning("Action %s rejected: %s", choice, error)
                print(error)
