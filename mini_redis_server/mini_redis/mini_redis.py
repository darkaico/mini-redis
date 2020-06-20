
class MiniRedis:

    def set(self, key, value: str, expiration: int = None):
        pass

    def get(self, key):
        pass

    def delete(self, key):
        pass

    def dbsize(self):
        pass

    def increment(self, key):
        pass

    def zadd(self, key, score, member):
        pass

    def zcard(self, key):
        pass

    def zrank(self, key, member):
        pass

    def zrange(self, start, stop):
        pass
