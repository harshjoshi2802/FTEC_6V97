class TrackerError(Exception):
    pass


class InvalidInputError(TrackerError):
    pass


class DuplicateError(TrackerError):
    pass


class NotFoundError(TrackerError):
    pass


class NoPortfolioSelectedError(TrackerError):
    pass


class InsufficientFundsError(TrackerError):
    pass


class InsufficientSharesError(TrackerError):
    pass


class PortfolioNotEmptyError(TrackerError):
    pass
