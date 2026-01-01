import redis
from src.config import Config

JTI_EXPIRY = 3600

token_blocklist = redis.from_url(Config.REDIS_URL)

print(token_blocklist.ping())


async def add_jti_to_blocklist(jti: str) -> None:
    token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti: str) -> bool:
    jti = token_blocklist.get(jti)

    return jti is not None
