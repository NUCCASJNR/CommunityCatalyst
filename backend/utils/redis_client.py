import redis
import json
from uuid import uuid4
from typing import Optional


def generate_auth_token() -> str:
    """
    Generates an authentication token
    :return: A unique authentication token
    """
    token = str(uuid4())
    return token


class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, key: str) -> Optional[str]:
        """
        Retrieves a value from Redis based on the provided key
        :param key: The key to retrieve
        :return: The retrieved value if it exists, or None
        """
        auth_key = f"auth_{key}"
        cached_data = self.redis_client.get(auth_key)
        if cached_data:
            return cached_data.decode('utf-8')
        return None

    def set(self, key: str, expiration: int, user_id: str):
        """
        Sets a key-value pair in Redis with an expiration time
        :param key: The key for the session data
        :param expiration: The expiration time in seconds
        :param user_id: The user ID to associate with the session
        """
        auth_key = f"auth_{key}"
        self.redis_client.setex(auth_key, expiration, user_id)
