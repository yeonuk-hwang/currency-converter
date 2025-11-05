from dataclasses import dataclass
from enum import Enum

from cur.core.exception import ParseError


@dataclass(frozen=True)
class CurrencyInfo:
    code: str
    korean_name: str
    subunit_name: str | None = None

    def __str__(self) -> str:
        return self.code


class Currency(Enum):
    AUD = CurrencyInfo("AUD", "달러", "센트")
    KRW = CurrencyInfo("KRW", "원", None)
    USD = CurrencyInfo("USD", "달러", "센트")

    @classmethod
    def from_string(cls, currency: str) -> "Currency":
        currency = currency.strip().upper()
        try:
            return cls[currency]
        except KeyError:
            supported = ", ".join(c.code for c in cls)
            raise ParseError(
                f"Unsupported currency: {currency}. Supported: {supported}"
            )

    @property
    def code(self) -> str:
        return self.value.code

    @property
    def korean_name(self) -> str:
        return self.value.korean_name

    @property
    def subunit_name(self) -> str | None:
        return self.value.subunit_name

    def __str__(self) -> str:
        return self.code
