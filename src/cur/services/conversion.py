from dataclasses import dataclass

from cur.adapters.exchange_rate_client import ExchangeRateClient
from cur.core.entity import Currency


@dataclass(frozen=True)
class ConversionResult:
    base_amount: float
    base_currency: str

    target_amount: float
    target_currency: str

    exchange_rate: float

    def __str__(self) -> str:
        return (
            f"{self.base_amount:,.2f} {self.base_currency} = "
            f"{self.target_amount:,.2f} {self.target_currency}"
            f" exchange rate: {self.exchange_rate}"
        )


class ConversionService:
    _client: ExchangeRateClient

    def __init__(self, exchange_rate_client: ExchangeRateClient) -> None:
        self._client = exchange_rate_client

    def convert(
        self, base_amount: float, base_currency: Currency, target_currency: Currency
    ) -> float:
        exchange_rate = self._client.get_rate(base_currency, target_currency)
        target_amount = base_amount * exchange_rate

        return ConversionResult(
            base_amount=base_amount,
            base_currency=base_currency.value,
            target_amount=target_amount,
            target_currency=target_currency.value,
            exchange_rate=exchange_rate,
        )
