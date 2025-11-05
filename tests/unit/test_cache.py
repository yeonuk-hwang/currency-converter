import time
from pathlib import Path

import pytest

from cur.adapters.cache import CachedData, ExchangeRateCache, FileCacheStorage


class TestCachedData:
    def test_is_expired_returns_true_when_past_expiry(self):
        past_time = int(time.time()) - 100
        cached = CachedData(data={"test": "data"}, ttl=past_time)

        assert cached.is_expired() is True

    def test_is_expired_returns_false_when_before_expiry(self):
        future_time = int(time.time()) + 100
        cached = CachedData(data={"test": "data"}, ttl=future_time)

        assert cached.is_expired() is False

    def test_to_dict_and_from_dict_roundtrip(self):
        original = CachedData(data={"key": "value"}, ttl=1234567890)

        as_dict = original.to_dict()
        restored = CachedData.from_dict(as_dict)

        assert restored == original


class TestFileCacheStorage:
    @pytest.fixture()
    def temp_cache_dir(self, tmp_path: Path) -> Path:
        return tmp_path / "currency-translator-test-cache"

    @pytest.fixture
    def storage(self, temp_cache_dir: Path) -> FileCacheStorage:
        return FileCacheStorage(cache_dir=temp_cache_dir)

    def test_init_creates_cache_directory(self, temp_cache_dir: Path):
        FileCacheStorage(cache_dir=temp_cache_dir)

        assert temp_cache_dir.exists()
        assert temp_cache_dir.is_dir()

    def test_read_returns_none_for_missing_key(self, storage: FileCacheStorage):
        result = storage.read("nonexistent")

        assert result is None

    def test_write_and_read_returns_data(self, storage: FileCacheStorage):
        test_data = {"rate": 1.23, "currency": "USD"}

        storage.write("USD", test_data)
        result = storage.read("USD")

        assert result == test_data

    def test_write_creates_file(self, storage: FileCacheStorage, temp_cache_dir: Path):
        test_data = {"rate": 1.23}

        storage.write("USD", test_data)

        cache_file = temp_cache_dir / "USD.json"
        assert cache_file.exists()

    def test_delete_removes_file(self, storage: FileCacheStorage, temp_cache_dir: Path):
        test_data = {"rate": 1.23}
        storage.write("USD", test_data)

        storage.delete("USD")

        cache_file = temp_cache_dir / "USD.json"
        assert not cache_file.exists()

    def test_list_keys_returns_all_keys(self, storage: FileCacheStorage):
        storage.write("USD", {"rate": 1.0})
        storage.write("KRW", {"rate": 1300.0})
        storage.write("AUD", {"rate": 1.5})

        keys = storage.list_keys()

        assert set(keys) == {"USD", "KRW", "AUD"}

    def test_handles_corrupted_file(
        self, storage: FileCacheStorage, temp_cache_dir: Path
    ):
        cache_file = temp_cache_dir / "CORRUPTED.json"
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text("invalid json content")

        result = storage.read("CORRUPTED")

        assert result is None
        assert not cache_file.exists()  # Should be removed

    def test_safe_key_conversion_slash(
        self, storage: FileCacheStorage, temp_cache_dir: Path
    ):
        test_data = {"rate": 1.23}
        key_with_slashes = "USD/EUR"

        storage.write(key_with_slashes, test_data)
        result = storage.read(key_with_slashes)

        assert result == test_data
        safe_files = list(temp_cache_dir.glob("*.json"))
        assert safe_files[0] == temp_cache_dir / "USD_EUR.json"

    def test_safe_key_conversion_backslash(
        self, storage: FileCacheStorage, temp_cache_dir: Path
    ):
        test_data = {"rate": 1.23}
        key_with_backslash = "USD\\EUR"

        storage.write(key_with_backslash, test_data)
        result = storage.read(key_with_backslash)

        assert result == test_data
        safe_files = list(temp_cache_dir.glob("*.json"))
        assert safe_files[0] == temp_cache_dir / "USD_EUR.json"


class TestExchangeRateCache:
    @pytest.fixture
    def temp_cache_dir(self, tmp_path: Path):
        return tmp_path / "cache"

    @pytest.fixture
    def cache(self, temp_cache_dir: Path) -> ExchangeRateCache:
        storage = FileCacheStorage(cache_dir=temp_cache_dir)
        return ExchangeRateCache(storage=storage)

    def test_get_returns_none_for_missing_key(self, cache: ExchangeRateCache):
        result = cache.get("nonexistent")

        assert result is None

    def test_set_and_get_returns_cached_data(self, cache: ExchangeRateCache):
        test_data = {"rate": 1.23, "currency": "USD"}
        future_expiry = int(time.time()) + 1000
        key = "USD"

        cache.set(key, test_data, future_expiry)
        result = cache.get(key)

        assert result == test_data

    def test_get_returns_none_for_expired_data(self, cache: ExchangeRateCache):
        test_data = {"rate": 1.23}
        past_expiry = int(time.time()) - 1
        key = "USD"

        cache.set(key, test_data, past_expiry)
        result = cache.get(key)

        assert result is None

    def test_clear_removes_all_entries(self, cache: ExchangeRateCache):
        future_expiry = int(time.time()) + 1000
        cache.set("USD", {"rate": 1.0}, future_expiry)
        cache.set("KRW", {"rate": 1300.0}, future_expiry)

        cache.clear()

        assert cache.get("USD") is None
        assert cache.get("KRW") is None

    def test_handles_invalid_cache_format(
        self, cache: ExchangeRateCache, temp_cache_dir: Path
    ):
        storage = FileCacheStorage(cache_dir=temp_cache_dir)
        storage.write("INVALID", {"wrong": "format"})  # Missing data/expiry_unix

        result = cache.get("INVALID")

        assert result is None
