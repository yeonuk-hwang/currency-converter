import time
from unittest.mock import Mock

import pytest
from httpx import Client, Response

from cur.adapters.cache import CacheStorage, ExchangeRateCache
from cur.adapters.exchange_rate_client import ExchangeRateClient
from cur.core.entity import Currency


class InMemoryStorage(CacheStorage):
    """Mock storage for testing cache behavior."""

    def __init__(self) -> None:
        self._data: dict[str, dict] = {}

    def read(self, key: str) -> dict | None:
        return self._data.get(key)

    def write(self, key: str, data: dict) -> None:
        self._data[key] = data

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def list_keys(self) -> list[str]:
        return list(self._data.keys())


class TestExchangeRateClientWithCache:
    @staticmethod
    def _setup_mock_response(mock_http_client: Mock, response_data: dict) -> None:
        """Helper to setup mock HTTP response."""
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = response_data
        mock_http_client.get.return_value = mock_response

    @pytest.fixture
    def mock_api_response(self) -> dict:
        """Mock API response data."""
        return {
            "result": "success",
            "time_last_update_unix": int(time.time()) - 3600,
            "time_next_update_unix": int(time.time()) + 82800,  # ~23 hours from now
            "base_code": "USD",
            "rates": {
                "USD": 1.0,
                "EUR": 0.9,
                "KRW": 1300.0,
                "AUD": 1.5,
            },
        }

    @pytest.fixture
    def mock_storage(self) -> InMemoryStorage:
        """Mock storage for cache testing."""
        return InMemoryStorage()

    @pytest.fixture
    def cache(self, mock_storage: InMemoryStorage) -> ExchangeRateCache:
        """Cache with mock storage."""
        return ExchangeRateCache(storage=mock_storage)

    @pytest.fixture
    def mock_http_client(self) -> Mock:
        """Mock HTTP client for testing."""
        return Mock(spec=Client)

    @pytest.fixture
    def client(
        self, cache: ExchangeRateCache, mock_http_client: Mock
    ) -> ExchangeRateClient:
        """Exchange rate client with mock dependencies."""
        return ExchangeRateClient(cache=cache, http_client=mock_http_client)

    def test_client_uses_injected_cache(self, cache: ExchangeRateCache) -> None:
        """Test that client uses the injected cache."""
        client = ExchangeRateClient(cache=cache)

        assert client._cache is cache

    def test_client_creates_default_cache_when_none_provided(self) -> None:
        """Test that client creates default cache when none provided."""
        client = ExchangeRateClient()

        assert client._cache is not None
        assert isinstance(client._cache, ExchangeRateCache)

    def test_client_uses_injected_http_client(self, mock_http_client: Mock) -> None:
        """Test that client uses the injected HTTP client."""
        client = ExchangeRateClient(http_client=mock_http_client)

        assert client._client is mock_http_client

    def test_client_creates_default_http_client_when_none_provided(self) -> None:
        """Test that client creates default HTTP client when none provided."""
        client = ExchangeRateClient()

        assert client._client is not None
        assert isinstance(client._client, Client)

    def test_get_rate_fetches_from_api_on_cache_miss(
        self,
        client: ExchangeRateClient,
        mock_http_client: Mock,
        mock_api_response: dict,
    ) -> None:
        """Test that client fetches from API when cache misses."""
        # Arrange
        self._setup_mock_response(mock_http_client, mock_api_response)

        # Act
        rate = client.get_rate(Currency.USD, Currency.KRW)

        # Assert
        assert rate == 1300.0
        mock_http_client.get.assert_called_once()

    def test_get_rate_uses_cache_on_second_call(
        self,
        client: ExchangeRateClient,
        mock_http_client: Mock,
        mock_api_response: dict,
    ) -> None:
        """Test that client uses cache on second call with same base currency."""
        # Arrange
        self._setup_mock_response(mock_http_client, mock_api_response)

        # Act - First call should hit API
        rate1 = client.get_rate(Currency.USD, Currency.KRW)
        # Second call should use cache (same base currency, different target)
        rate2 = client.get_rate(Currency.USD, Currency.AUD)

        # Assert
        assert rate1 == 1300.0
        assert rate2 == 1.5
        # API should only be called once (second call uses cached data)
        assert mock_http_client.get.call_count == 1

    def test_get_rate_caches_response_with_correct_ttl(
        self,
        client: ExchangeRateClient,
        cache: ExchangeRateCache,
        mock_http_client: Mock,
        mock_api_response: dict,
    ) -> None:
        """Test that client caches API response with correct TTL."""
        # Arrange
        self._setup_mock_response(mock_http_client, mock_api_response)

        # Act
        client.get_rate(Currency.USD, Currency.KRW)

        # Assert - Check cache has entry with correct data
        cached_data = cache.get("USD")
        assert cached_data is not None
        assert cached_data["base_code"] == "USD"
        assert cached_data["rates"]["KRW"] == 1300.0

    def test_get_rate_raises_value_error_for_currency_not_in_api_response(
        self, client: ExchangeRateClient, mock_http_client: Mock
    ) -> None:
        """Test that client raises ValueError when target currency not in API response."""
        # Arrange - Create a mock response that doesn't include KRW
        limited_response: dict = {
            "result": "success",
            "documentation": "https://www.exchangerate-api.com/docs",
            "terms_of_use": "https://www.exchangerate-api.com/terms",
            "time_last_update_unix": int(time.time()) - 3600,
            "time_last_update_utc": "Thu, 01 Jan 2024 00:00:00 +0000",
            "time_next_update_unix": int(time.time()) + 82800,
            "time_next_update_utc": "Fri, 02 Jan 2024 00:00:00 +0000",
            "base_code": "USD",
            "rates": {
                "USD": 1.0,
                "AUD": 1.5,
                # KRW is intentionally missing
            },
        }
        self._setup_mock_response(mock_http_client, limited_response)

        # Act & Assert
        with pytest.raises(ValueError, match="not found in rates"):
            client.get_rate(Currency.USD, Currency.KRW)

    def test_different_base_currencies_cache_separately(
        self,
        client: ExchangeRateClient,
        mock_http_client: Mock,
        mock_api_response: dict,
    ) -> None:
        """Test that different base currencies are cached separately."""
        # Arrange
        # Second response for AUD (different base currency)
        aud_response_data = mock_api_response.copy()
        aud_response_data["base_code"] = "AUD"
        aud_response_data["rates"] = {
            "USD": 0.67,
            "AUD": 1.0,
            "KRW": 870.0,
        }

        # Setup multiple responses
        usd_response = Mock(spec=Response)
        usd_response.json.return_value = mock_api_response
        aud_response = Mock(spec=Response)
        aud_response.json.return_value = aud_response_data
        mock_http_client.get.side_effect = [usd_response, aud_response]

        # Act
        rate1 = client.get_rate(Currency.USD, Currency.KRW)
        rate2 = client.get_rate(Currency.AUD, Currency.KRW)

        # Assert
        assert rate1 == 1300.0  # From USD base
        assert rate2 == 870.0  # From AUD base
        assert mock_http_client.get.call_count == 2  # Both should hit API
