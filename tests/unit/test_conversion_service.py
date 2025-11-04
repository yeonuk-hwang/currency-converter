import pytest

from cur.core.entity import Currency
from cur.services.conversion import ConversionResult, ConversionService

MOCK_RATE = 935.5


class TestExchangeRateClient:
    def get_rate(self, base_currency: Currency, target_currency: Currency) -> float:
        return MOCK_RATE


@pytest.fixture(scope="module")
def client() -> TestExchangeRateClient:
    return TestExchangeRateClient()


@pytest.fixture(scope="function")
def service(client: TestExchangeRateClient) -> ConversionService:
    return ConversionService(client)


def test_conversion_service_can_convert(service: ConversionService):
    aud = Currency.AUD
    aud_amount = 1000

    krw = Currency.KRW
    expected_krw_amount = aud_amount * MOCK_RATE

    expected_conversion_result = ConversionResult(
        base_amount=aud_amount,
        base_currency=aud.code,
        target_currency=krw.code,
        target_amount=expected_krw_amount,
        exchange_rate=MOCK_RATE,
    )

    conversion_result = service.convert(aud_amount, aud, krw)

    assert conversion_result == expected_conversion_result
