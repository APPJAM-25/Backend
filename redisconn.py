import os
from dotenv import load_dotenv
import redis

load_dotenv()


def redisConfig():
    try:
        REDIS_HOST = os.getenv("REDIS_HOST")
        REDIS_PORT = os.getenv("REDIS_PORT")
        REDIS_DATABASE = os.getenv("REDIS_DATABASE")
        rd = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DATABASE)

        return rd
    except:
        raise Exception("Redis Connection Error")
