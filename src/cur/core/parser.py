import re
from enum import Enum, IntEnum
from typing import Final


class ParseError(Exception):
    pass


class UnitMultiplier(IntEnum):
    K = 1_000
    M = 1_000_000
    B = 1_000_000_000

    @classmethod
    def from_string(cls, unit: str) -> int:
        try:
            return cls[unit.upper()].value
        except KeyError:
            raise ParseError(f"Invalid unit: {unit}")


class Currency(Enum):
    AUD = "AUD"
    KRW = "KRW"
    USD = "USD"

    @classmethod
    def from_string(cls, currency: str) -> str:
        currency = currency.strip().upper()
        try:
            return cls[currency].value
        except KeyError:
            supported = ", ".join(c.value for c in cls)
            raise ParseError(
                f"Unsupported currency: {currency}. Supported: {supported}"
            )


AMOUNT_PATTERN: Final[re.Pattern] = re.compile(
    r"^(\d+\.?\d*|\.\d+)([kmb])?$", re.IGNORECASE
)


def parse_amount(amount: str) -> float:
    if not amount or not amount.strip():
        raise ParseError("Amount cannot be empty")

    amount_clean = amount.strip().replace(",", "")

    match = AMOUNT_PATTERN.match(amount_clean)
    if not match:
        raise ParseError(f"Invalid amount format: {amount}")

    number_str, unit = match.groups()

    try:
        number = float(number_str)
    except ValueError:
        raise ParseError(f"Invalid number: {number_str}")

    if unit:
        number *= UnitMultiplier.from_string(unit)

    if number == 0:
        raise ParseError("Amount must be greater than zero")
    if number < 0:
        raise ParseError("Amount must be positive")

    return number


def parse_currency(currency: str) -> str:
    return Currency.from_string(currency)
