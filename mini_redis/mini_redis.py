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

    def get(self, key: str):
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

    def dbsize(self):
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

    def zadd(self, key: str, score, member):
        if key not in self._kv_ordered_store:
            self._kv_ordered_store[key] = []

        self._kv_ordered_store[key].insert(score, member)

        # TODO: verify doc
        return 1

    def zcard(self, key: str):
        zlist = self._kv_ordered_store.get(key, [])

        return len(zlist)

    def zrank(self, key: str, member):
        zlist = self._kv_ordered_store.get(key, [])

        if member not in zlist:
            return None

        return zlist.index(member)

    def zrange(self, key: str, start: int, stop: int):
        zlist = self._kv_ordered_store.get(key)
        if not zlist:
            return []

        zlen = len(zlist)

        if start > zlen or (stop >= 0 and start > stop):
            return []

        stop_index = stop % zlen + 1
        return zlist[start:stop_index]
