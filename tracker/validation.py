from decimal import Decimal, InvalidOperation

from .errors import InvalidInputError


def required_text(value, label):
    value = value.strip()
    if not value:
        raise InvalidInputError(f"{label} cannot be blank.")
    return value


def number(value, label, allow_zero=False):
    try:
        result = Decimal(str(value))
    except InvalidOperation as error:
        raise InvalidInputError(f"{label} must be a number.") from error
    if not result.is_finite():
        raise InvalidInputError(f"{label} must be a finite number.")
    if result < 0 or (result == 0 and not allow_zero):
        rule = "zero or more" if allow_zero else "greater than zero"
        raise InvalidInputError(f"{label} must be {rule}.")
    return result


def share_quantity(value):
    result = number(value, "Quantity")
    if result != result.to_integral_value():
        raise InvalidInputError("Quantity must be a whole number of shares.")
    return int(result)
