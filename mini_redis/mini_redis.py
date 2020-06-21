from mini_redis.data_stores import SortedList
from utils import data_utils
from utils.singleton import SingletonMixin


class CommandError(Exception):
    pass


class MiniRedis(SingletonMixin):

    _kv_store = None
    _kv_ordered_store = None

    OK = 'OK'

    def __init__(self):
        self._kv_store = {}
        self._kv_ordered_store = {}

    def set(self, key: str, value: str, expiration: int = None):
        self._kv_store[key] = value

        return self.OK

    def get(self, key: str) -> str:
        if key in self._kv_ordered_store:
            raise CommandError

        return self._kv_store.get(key)

    def delete(self, key: str):
        if key in self._kv_store:
            del self._kv_store[key]
        elif key in self._kv_ordered_store:
            del self._kv_ordered_store[key]
        else:
            return None

        return self.OK

    def dbsize(self) -> int:
        return len(self._kv_store.keys()) + len(self._kv_ordered_store.keys())

    def incr(self, key: str):
        value = self._kv_store.get(key)
        if not value:
            self._kv_store[key] = 1
            return self.OK

        if not data_utils.is_integer(value):
            raise CommandError

        self._kv_store[key] = int(value) + 1

        return self.OK

    def zadd(self, key: str, score: float, member: str) -> int:

        if not data_utils.is_float(score):
            raise CommandError('value is not a valid float')

        if key not in self._kv_ordered_store:
            self._kv_ordered_store[key] = SortedList()

        sorted_list = self._kv_ordered_store[key]

        return sorted_list.zadd(score, member)

    def zcard(self, key: str) -> int:
        sorted_list = self._kv_ordered_store.get(key)
        if not sorted_list:
            return 0

        return sorted_list.zcard()

    def zrank(self, key: str, member) -> int:
        sorted_list = self._kv_ordered_store.get(key)

        if not sorted_list:
            return None

        return sorted_list.zrank(member)

    def zrange(self, key: str, start: int, stop: int) -> list:
        if not data_utils.is_integer(start) or not data_utils.is_integer(stop):
            raise CommandError('value is not an integer or out of range')

        sorted_list = self._kv_ordered_store.get(key)
        if not sorted_list:
            return []

        return sorted_list.zrange(start, stop)
