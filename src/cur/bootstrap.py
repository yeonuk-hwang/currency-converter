import os
from pathlib import Path

from cur.adapters.cache import ExchangeRateCache, FileCacheStorage
from cur.adapters.exchange_rate_client import ExchangeRateClient
from cur.services.conversion import ConversionService


def bootstrap() -> ConversionService:
    cache_dir_env = os.getenv("CURRENCY_TRANSLATOR_CACHE_DIR")
    cache_dir = Path(cache_dir_env) if cache_dir_env else None

    storage = FileCacheStorage(cache_dir)
    cache = ExchangeRateCache(storage)
    exchange_rate_client = ExchangeRateClient(cache)
    conversion_service = ConversionService(exchange_rate_client)

    return conversion_service
