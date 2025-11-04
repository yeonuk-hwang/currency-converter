import os

import pytest

from cur.adapters.exchange_rate_client import ExchangeRateClient
from cur.core.entity import Currency


@pytest.fixture(scope="session")
def client() -> ExchangeRateClient:
    api_key = os.getenv("API_KEY")
    return ExchangeRateClient(api_key)


def test_get_aud_to_krw(client: ExchangeRateClient):
    aud = Currency.AUD
    krw = Currency.KRW
    rate = client.get_rate(aud, krw)

    assert rate is not None
    assert isinstance(rate, float)
    assert rate > 0


def test_get_krw_to_aud(client: ExchangeRateClient):
    aud = Currency.AUD
    krw = Currency.KRW
    rate = client.get_rate(krw, aud)

    assert rate is not None
    assert isinstance(rate, float)
    assert rate > 0
