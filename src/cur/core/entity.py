from dataclasses import dataclass
from enum import Enum

from cur.core.exception import ParseError


@dataclass(frozen=True)
class CurrencyInfo:
    code: str
    korean_name: str

    def __str__(self) -> str:
        return self.code


class Currency(Enum):
    AUD = CurrencyInfo("AUD", "호주 달러")
    KRW = CurrencyInfo("KRW", "원")
    USD = CurrencyInfo("USD", "미국 달러")

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

    def __str__(self) -> str:
        return self.code
