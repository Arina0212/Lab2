import json
import logging
import os
from typing import Any

from redis import Redis
from redis.asyncio import Redis as AsyncRedis
from redis.exceptions import RedisError

logger = logging.getLogger(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
USER_CACHE_TTL_SECONDS = int(os.getenv("USER_CACHE_TTL_SECONDS", "3600"))
PRODUCT_CACHE_TTL_SECONDS = int(os.getenv("PRODUCT_CACHE_TTL_SECONDS", "600"))

_async_client: AsyncRedis | None = None
_sync_client: Redis | None = None

_USER_CACHE_PREFIX = "users:detail:"
_PRODUCT_CACHE_PREFIX = "products:detail:"
_PRODUCT_LIST_CACHE_KEY = "products:list"


def _user_cache_key(user_id: int) -> str:
    return f"{_USER_CACHE_PREFIX}{user_id}"


def _product_cache_key(product_id: int) -> str:
    return f"{_PRODUCT_CACHE_PREFIX}{product_id}"


def get_async_client() -> AsyncRedis | None:
    global _async_client
    if _async_client is None:
        _async_client = AsyncRedis.from_url(
            REDIS_URL, decode_responses=True
        )
    return _async_client


def get_sync_client() -> Redis | None:
    global _sync_client
    if _sync_client is None:
        _sync_client = Redis.from_url(REDIS_URL, decode_responses=True)
    return _sync_client


def reset_clients() -> None:
    """Reset cached Redis clients (primarily for tests)."""
    global _async_client, _sync_client
    _async_client = None
    _sync_client = None


def _loads(value: str | None) -> Any:
    if not value:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        logger.warning("Failed to decode cached payload: %s", value)
        return None


def _dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


async def get_cached_user(user_id: int) -> dict[str, Any] | None:
    client = get_async_client()
    if not client:
        return None
    try:
        cached = await client.get(_user_cache_key(user_id))
    except (RedisError, RuntimeError) as exc:
        logger.warning("Redis unavailable, skip user cache read: %s", exc)
        return None
    return _loads(cached)


async def cache_user(user_id: int, payload: dict[str, Any]) -> None:
    client = get_async_client()
    if not client:
        return
    try:
        await client.set(
            _user_cache_key(user_id),
            _dumps(payload),
            ex=USER_CACHE_TTL_SECONDS,
        )
    except (RedisError, RuntimeError) as exc:
        logger.warning("Redis unavailable, skip user cache write: %s", exc)


async def invalidate_user_cache(user_id: int) -> None:
    client = get_async_client()
    if not client:
        return
    try:
        await client.delete(_user_cache_key(user_id))
    except (RedisError, RuntimeError) as exc:
        logger.warning("Redis unavailable, skip user cache invalidation: %s", exc)


def get_cached_products() -> list[dict[str, Any]] | None:
    client = get_sync_client()
    if not client:
        return None
    try:
        cached = client.get(_PRODUCT_LIST_CACHE_KEY)
    except RedisError as exc:
        logger.warning("Redis unavailable, skip product list cache read: %s", exc)
        return None
    return _loads(cached)


def cache_products(payload: list[dict[str, Any]]) -> None:
    client = get_sync_client()
    if not client:
        return
    try:
        client.set(
            _PRODUCT_LIST_CACHE_KEY,
            _dumps(payload),
            ex=PRODUCT_CACHE_TTL_SECONDS,
        )
    except RedisError as exc:
        logger.warning("Redis unavailable, skip product list cache write: %s", exc)


def invalidate_products_cache() -> None:
    client = get_sync_client()
    if not client:
        return
    try:
        client.delete(_PRODUCT_LIST_CACHE_KEY)
    except RedisError as exc:
        logger.warning("Redis unavailable, skip product list cache delete: %s", exc)


def get_cached_product(product_id: int) -> dict[str, Any] | None:
    client = get_sync_client()
    if not client:
        return None
    try:
        cached = client.get(_product_cache_key(product_id))
    except RedisError as exc:
        logger.warning("Redis unavailable, skip product cache read: %s", exc)
        return None
    return _loads(cached)


def cache_product(product_id: int, payload: dict[str, Any]) -> None:
    client = get_sync_client()
    if not client:
        return
    try:
        client.set(
            _product_cache_key(product_id),
            _dumps(payload),
            ex=PRODUCT_CACHE_TTL_SECONDS,
        )
    except RedisError as exc:
        logger.warning("Redis unavailable, skip product cache write: %s", exc)


def invalidate_product(product_id: int) -> None:
    client = get_sync_client()
    if not client:
        return
    try:
        client.delete(_product_cache_key(product_id))
    except RedisError as exc:
        logger.warning("Redis unavailable, skip product cache delete: %s", exc)

