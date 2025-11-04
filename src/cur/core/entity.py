from enum import Enum

from cur.core.exception import ParseError


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
