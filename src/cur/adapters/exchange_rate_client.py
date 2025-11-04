from dataclasses import dataclass
from typing import Literal

from httpx import Client


@dataclass
class PairExchangeRateResponse:
    result: Literal["success", "error"]
    documentation: str
    terms_of_use: str
    time_last_update_unix: int
    time_last_update_utc: str
    time_next_update_unix: int
    time_next_update_utc: str
    base_code: str
    target_code: str
    conversion_rate: float

    @classmethod
    def from_dict(cls, data: dict) -> "PairExchangeRateResponse":
        return cls(
            result=data["result"],
            documentation=data["documentation"],
            terms_of_use=data["terms_of_use"],
            time_last_update_unix=data["time_last_update_unix"],
            time_last_update_utc=data["time_last_update_utc"],
            time_next_update_unix=data["time_next_update_unix"],
            time_next_update_utc=data["time_next_update_utc"],
            base_code=data["base_code"],
            target_code=data["target_code"],
            conversion_rate=data["conversion_rate"],
        )


class ExchangeRateClient:
    _client: Client
    _api_key: str

    def __init__(self, api_key: str) -> None:
        self._client = Client(base_url="https://v6.exchangerate-api.com/v6/")
        self._api_key = api_key
        pass

    def get_rate(self, base_currency: str, target_currency: str) -> float:
        api_path = (
            f"{self._api_key}/pair/{base_currency.upper()}/{target_currency.upper()}"
        )
        response = self._client.get(url=api_path)
        response.raise_for_status()
        api_response_raw = response.json()

        api_response = PairExchangeRateResponse.from_dict(api_response_raw)

        return api_response.conversion_rate
