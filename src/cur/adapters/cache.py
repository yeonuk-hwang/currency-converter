import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from platformdirs import user_cache_dir


@dataclass
class CachedData:
    data: dict
    expiry_unix: int

    def is_expired(self) -> bool:
        return int(time.time()) >= self.expiry_unix

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CachedData":
        return cls(data=data["data"], expiry_unix=data["expiry_unix"])


class CacheStorage(Protocol):
    def read(self, key: str) -> dict | None: ...

    def write(self, key: str, data: dict) -> None: ...

    def delete(self, key: str) -> None: ...

    def list_keys(self) -> list[str]: ...


class FileCacheStorage(CacheStorage):
    def __init__(self, cache_dir: Path | None = None) -> None:
        if cache_dir is None:
            cache_dir = Path(user_cache_dir("currency-translator"))

        self._cache_dir = cache_dir
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        safe_key = key.replace("/", "_").replace("\\", "_")
        return self._cache_dir / f"{safe_key}.json"

    def read(self, key: str) -> dict | None:
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            with cache_path.open("r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            self.delete(key)
            return None

    def write(self, key: str, data: dict) -> None:
        cache_path = self._get_cache_path(key)
        with cache_path.open("w") as f:
            json.dump(data, f, indent=2)

    def delete(self, key: str) -> None:
        cache_path = self._get_cache_path(key)
        cache_path.unlink(missing_ok=True)

    def list_keys(self) -> list[str]:
        if not self._cache_dir.exists():
            return []

        keys = []
        for cache_file in self._cache_dir.glob("*.json"):
            keys.append(cache_file.stem)
        return keys


class ExchangeRateCache:
    def __init__(self, storage: CacheStorage | None = None) -> None:
        self._storage = storage if storage is not None else FileCacheStorage()

    def get(self, key: str) -> dict | None:
        raw_data = self._storage.read(key)
        if raw_data is None:
            return None

        try:
            cached = CachedData.from_dict(raw_data)

            if cached.is_expired():
                self._storage.delete(key)
                return None

            return cached.data

        except (KeyError, TypeError):
            self._storage.delete(key)
            return None

    def set(self, key: str, data: dict, expiry_unix: int) -> None:
        cached = CachedData(data=data, expiry_unix=expiry_unix)
        self._storage.write(key, cached.to_dict())

    def clear(self) -> None:
        for key in self._storage.list_keys():
            self._storage.delete(key)
