import redis
from typing import Optional

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.StrictRedis(host=host, port=port, db=db)

    def get_payment_info(self, key: str) -> Optional[dict]:
        """
        Retrieves payment information (project ID, amount, and reference) from Redis based on the provided key
        :param key: The key to retrieve payment information
        :return: The retrieved payment information as a dictionary if it exists, or None
        """
        payment_key = f"payment_info_{key}"
        payment_info = self.redis_client.get(payment_key)
        if payment_info:
            return json.loads(payment_info.decode('utf-8'))
        return None

    def set_payment_info(self, key: str, project_id: int, amount: float, reference: str, expiration: int):
        """
        Sets payment information in Redis with an expiration time
        :param key: The key for the payment information
        :param project_id: The project ID
        :param amount: The payment amount
        :param reference: The payment reference to store
        :param expiration: The expiration time in seconds
        """
        payment_key = f"payment_info_{key}"
        payment_data = {
            "project_id": project_id,
            "amount": amount,
            "reference": reference
        }
        self.redis_client.setex(payment_key, expiration, json.dumps(payment_data))
