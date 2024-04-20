import os
from dotenv import load_dotenv
import redis

load_dotenv()


class Redis:
    def __init__(self):
        self.host = os.getenv("REDIS_HOST")
        self.port = os.getenv("REDIS_PORT")
        self.db = os.getenv("REDIS_DATABASE")
        self.rd = redis.Redis(host=self.host, port=self.port, db=self.db)

    def __call__(self):
        return self.rd
