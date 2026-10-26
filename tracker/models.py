from decimal import Decimal


class Asset:
    def __init__(self, ticker, name):
        self.ticker = ticker
        self.name = name


class Position:
    def __init__(self, quantity=0, average_cost=Decimal("0")):
        self.quantity = quantity
        self.average_cost = average_cost


class Trade:
    def __init__(self, side, ticker, quantity, price):
        self.side = side
        self.ticker = ticker
        self.quantity = quantity
        self.price = price


class Portfolio:
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.positions = {}
        self.trades = []
        self.realized_gain = Decimal("0")
