from dataclasses import asdict, dataclass
from typing import Literal

from httpx import Client

from cur.adapters.cache import ExchangeRateCache
from cur.core.entity import Currency


@dataclass
class LatestExchangeRateResponse:
    result: Literal["success", "error"]
    documentation: str
    terms_of_use: str
    time_last_update_unix: int
    time_last_update_utc: str
    time_next_update_unix: int
    time_next_update_utc: str
    base_code: str
    conversion_rates: dict[str, float]

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "LatestExchangeRateResponse":
        return cls(
            result=data["result"],
            documentation=data["documentation"],
            terms_of_use=data["terms_of_use"],
            time_last_update_unix=data["time_last_update_unix"],
            time_last_update_utc=data["time_last_update_utc"],
            time_next_update_unix=data["time_next_update_unix"],
            time_next_update_utc=data["time_next_update_utc"],
            base_code=data["base_code"],
            conversion_rates=data["conversion_rates"],
        )


class ExchangeRateClient:
    def __init__(
        self,
        cache: ExchangeRateCache | None = None,
        http_client: Client | None = None,
    ) -> None:
        self._client = http_client or Client(
            base_url="https://v6.exchangerate-api.com/v6/"
        )
        self._cache = cache if cache is not None else ExchangeRateCache()

    def _get_latest_rates(self, base_currency: Currency) -> LatestExchangeRateResponse:
        cache_key = base_currency.code

        cached_data = self._cache.get(cache_key)
        if cached_data is not None:
            return LatestExchangeRateResponse.from_dict(cached_data)

        api_path = f"/latest/{base_currency}"
        response = self._client.get(url=api_path)
        response.raise_for_status()
        api_response_raw = response.json()

        api_response = LatestExchangeRateResponse.from_dict(api_response_raw)

        self._cache.set(
            cache_key, api_response.to_dict(), api_response.time_next_update_unix
        )

        return api_response

    def get_rate(self, base_currency: Currency, target_currency: Currency) -> float:
        latest_rates = self._get_latest_rates(base_currency)
        target_code = target_currency.code

        if target_code not in latest_rates.conversion_rates:
            raise ValueError(f"Target currency {target_code} not found in rates")

        return latest_rates.conversion_rates[target_code]
