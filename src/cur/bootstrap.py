from cur.adapters.exchange_rate_client import ExchangeRateClient
from cur.services.conversion import ConversionService


def bootstrap() -> ConversionService:
    exchange_rate_client = ExchangeRateClient()
    conversion_service = ConversionService(exchange_rate_client)

    return conversion_service
