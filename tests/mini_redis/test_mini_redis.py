import pytest

from mini_redis_server.mini_redis import MiniRedis


@pytest.fixture
def mini_redis():
    return MiniRedis()


def test_set_get(mini_redis):
    mini_redis.set('wolverine', 'Guepardo')

    assert mini_redis.get('wolverine') == 'Guepardo'


def test_set_get_delete(mini_redis):
    mini_redis.set('cyclop', 'Ciclope')
    assert mini_redis.get('cyclop') == 'Ciclope'

    mini_redis.delete('cyclope')

    assert mini_redis.get('cyclop') is None


def test_twice_set_get(mini_redis):
    mini_redis.set('wolverine', 'Guepardo')
    mini_redis.set('wolverine', 'Wolverio')

    assert mini_redis.get('wolverine') == 'Wolverio'


def test_dbsize(mini_redis):
    mini_redis.set('cyclop', 'Ciclope')
    mini_redis.set('cyclop', 'Cyclop')
    mini_redis.set('wolverine', 'Guepardo')
    mini_redis.set('gambit', 'Gambito')

    assert mini_redis.dbsize() == 3


def test_increment_no_key(mini_redis):
    mini_redis.increment('mutants')

    assert mini_redis.get('mutants') == 0


def test_increment_valid_existing_key(mini_redis):
    mini_redis.set('mutants', 7)
    mini_redis.increment('mutants')

    assert mini_redis.get('mutants') == 8


def test_increment_invalid_case(mini_redis):
    mini_redis.set('mutant_houses', {'id': 2})

    with pytest.raises(CommandError):
        mini_redis.increment('mutant_houses')


def test_zadd_and_zrange(mini_redis):
    mini_redis.zadd('myzset', 1, 'one')
    mini_redis.zadd('myzset', 1, 'uno')
    mini_redis.zadd('myzset', 2, 'two')
    mini_redis.zadd('myzset', 3, 'three')

    assert mini_redis.zrange('myzset', 0, -1) == ['one', 'uno', 'two', 'three']


def test_zcard(mini_redis):
    mini_redis.zadd('myzset', 1, 'uno')
    mini_redis.zadd('myzset', 2, 'two')

    assert mini_redis.zcard('myzset') == 2


def test_zrank(mini_redis):
    mini_redis.zadd('myzset', 1, 'uno')
    mini_redis.zadd('myzset', 2, 'two')
    mini_redis.zadd('myzset', 3, 'three')

    assert mini_redis.zrank('three') == 2


def test_zrank_no_keys(mini_redis):
    assert mini_redis.zrank('four') is None
