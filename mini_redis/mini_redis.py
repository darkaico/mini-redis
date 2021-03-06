import threading

from mini_redis.data_stores import SortedList
from utils import data_utils
from utils.singleton import SingletonMixin


class CommandError(Exception):
    pass


class MiniRedis(SingletonMixin):

    _store_lock = threading.Lock()
    _kv_store = None
    _kv_ordered_store = None

    OK = 'OK'

    def __init__(self):
        self._kv_store = {}
        self._kv_ordered_store = {}

    def set(self, key: str, value: str, expiration: int = None):
        with self._store_lock:
            self._kv_store[key] = value

        return self.OK

    def get(self, key: str) -> str:
        if key in self._kv_ordered_store:
            raise CommandError('Operation against a key holding the wrong kind of value')

        return self._kv_store.get(key)

    def delete(self, key: str):
        if key in self._kv_store:
            with self._store_lock:
                del self._kv_store[key]
        elif key in self._kv_ordered_store:
            with self._store_lock:
                del self._kv_ordered_store[key]
        else:
            return None

        return self.OK

    def dbsize(self) -> int:
        return len(self._kv_store.keys()) + len(self._kv_ordered_store.keys())

    def incr(self, key: str):
        with self._store_lock:
            value = self._kv_store.get(key)
            if not value:
                self._kv_store[key] = 1
                return self.OK

            if not data_utils.is_integer(value):
                raise CommandError('value is not an integer or out of range')

            self._kv_store[key] = int(value) + 1

        return self.OK

    def zadd(self, key: str, score: float, member: str) -> int:

        if not data_utils.is_float(score):
            raise CommandError('value is not a valid float')

        with self._store_lock:
            if key not in self._kv_ordered_store:
                self._kv_ordered_store[key] = SortedList()

            sorted_list = self._kv_ordered_store[key]
            result = sorted_list.zadd(float(score), member)

        return result

    def zcard(self, key: str) -> int:
        if key in self._kv_store:
            raise CommandError('Operation against a key holding the wrong kind of value')

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

        return sorted_list.zrange(int(start), int(stop))
