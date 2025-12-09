from __future__ import annotations

import os
from typing import Any

import redis


def get_client() -> redis.Redis:
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(redis_url, decode_responses=True)


def section(title: str) -> None:
    print(f"\n{'=' * 10} {title} {'=' * 10}")


def demo_strings(client: redis.Redis) -> None:
    section("Strings")
    client.set("user:name", "Иван")
    print("user:name ->", client.get("user:name"))

    client.setex("session:123", 3600, "active")  # 1 hour TTL
    ttl = client.ttl("session:123")
    print("session:123 TTL:", ttl)

    client.set("counter", 0)
    client.incr("counter")
    client.incrby("counter", 5)
    client.decr("counter")
    print("counter ->", client.get("counter"))


def demo_lists(client: redis.Redis) -> None:
    section("Lists")
    client.delete("tasks")
    client.lpush("tasks", "task1", "task2")
    client.rpush("tasks", "task3", "task4")
    print("tasks ->", client.lrange("tasks", 0, -1))
    print("lpop ->", client.lpop("tasks"))
    print("rpop ->", client.rpop("tasks"))
    print("length ->", client.llen("tasks"))


def demo_sets(client: redis.Redis) -> None:
    section("Sets")
    client.delete("tags", "languages")
    client.sadd("tags", "python", "redis", "database")
    client.sadd("languages", "python", "java", "javascript")
    print("is python in tags?", client.sismember("tags", "python"))
    print("all tags ->", client.smembers("tags"))
    print("intersection ->", client.sinter("tags", "languages"))
    print("union ->", client.sunion("tags", "languages"))
    print("difference ->", client.sdiff("tags", "languages"))


def demo_hashes(client: redis.Redis) -> None:
    section("Hashes")
    client.delete("user:1000")
    client.hset(
        "user:1000",
        mapping={"name": "Иван", "age": "30", "city": "Москва"},
    )
    print("name ->", client.hget("user:1000", "name"))
    print("all ->", client.hgetall("user:1000"))
    print("email exists?", client.hexists("user:1000", "email"))
    print("keys ->", client.hkeys("user:1000"))
    print("values ->", client.hvals("user:1000"))


def demo_sorted_sets(client: redis.Redis) -> None:
    section("Sorted Sets")
    client.delete("leaderboard")
    client.zadd("leaderboard", {"player1": 100, "player2": 200, "player3": 150})
    print("top players ->", client.zrange("leaderboard", 0, 2, withscores=True))
    print("by score ->", client.zrangebyscore("leaderboard", 100, 200))
    print("player1 rank ->", client.zrank("leaderboard", "player1"))


def main() -> None:
    client = get_client()
    demo_strings(client)
    demo_lists(client)
    demo_sets(client)
    demo_hashes(client)
    demo_sorted_sets(client)


if __name__ == "__main__":
    main()

