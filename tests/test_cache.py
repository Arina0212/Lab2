import pytest

from app import cache


import pytest

pytestmark = pytest.mark.enable_redis


@pytest.fixture
def fake_sync_redis(monkeypatch):
    import fakeredis

    client = fakeredis.FakeStrictRedis(decode_responses=True)
    monkeypatch.setattr(cache, "_sync_client", client)
    yield client
    monkeypatch.setattr(cache, "_sync_client", None)


@pytest.fixture
def fake_async_redis(monkeypatch):
    import fakeredis.aioredis

    client = fakeredis.aioredis.FakeRedis(decode_responses=True)
    monkeypatch.setattr(cache, "_async_client", client)
    yield client
    monkeypatch.setattr(cache, "_async_client", None)


@pytest.mark.asyncio
async def test_user_cache_store_and_invalidate(fake_async_redis):
    payload = {"id": 1, "name": "Test"}

    await cache.cache_user(1, payload)
    cached = await cache.get_cached_user(1)
    assert cached == payload

    ttl = await fake_async_redis.ttl(cache._user_cache_key(1))
    assert ttl is None or (ttl <= cache.USER_CACHE_TTL_SECONDS and ttl > 0)

    await cache.invalidate_user_cache(1)
    assert await cache.get_cached_user(1) is None


def test_product_cache_store_and_invalidate(fake_sync_redis):
    products = [{"id": 1, "name": "P1"}]

    cache.cache_products(products)
    assert cache.get_cached_products() == products

    ttl = fake_sync_redis.ttl(cache._PRODUCT_LIST_CACHE_KEY)
    assert ttl is None or (ttl <= cache.PRODUCT_CACHE_TTL_SECONDS and ttl > 0)

    product_payload = {"id": 2, "name": "P2"}
    cache.cache_product(2, product_payload)
    assert cache.get_cached_product(2) == product_payload

    cache.invalidate_product(2)
    assert cache.get_cached_product(2) is None

    cache.invalidate_products_cache()
    assert cache.get_cached_products() is None

