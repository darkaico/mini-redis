import pytest

from mini_redis_server.mini_redis import (
    CommandError,
    MiniRedis
)


@pytest.fixture
def mini_redis():
    return MiniRedis()


@pytest.fixture
def mini_redis_with_mutants():
    mini_redis = MiniRedis()

    mini_redis.set('x1', 'Wolverine')
    mini_redis.set('x2', 'Gambit')
    mini_redis.set('x3', 'Quicksilver')

    return mini_redis


@pytest.fixture
def mini_redis_with_ordered_mutants():
    mini_redis = MiniRedis()

    mini_redis.zadd('mutants', 1, 'Wolverine')
    mini_redis.zadd('mutants', 1, 'Guepardo')
    mini_redis.zadd('mutants', 2, 'Gambit')
    mini_redis.zadd('mutants', 3, 'Quicksilver')

    return mini_redis


@pytest.fixture
def mini_redis_with_all_mutants(mini_redis_with_mutants):

    mini_redis_with_mutants.zadd('mutants', 1, 'Wolverine')
    mini_redis_with_mutants.zadd('mutants', 1, 'Guepardo')
    mini_redis_with_mutants.zadd('mutants', 2, 'Gambit')
    mini_redis_with_mutants.zadd('mutants', 3, 'Quicksilver')

    return mini_redis_with_mutants

# Basic Behavior


def test_set_basic(mini_redis):

    assert mini_redis.set('wolverine', 'Guepardo') == 'OK'


def test_get_basic(mini_redis):

    assert mini_redis.get('wolverine') is None


def test_delete_basic(mini_redis):

    assert mini_redis.delete('wolverine') is None


def test_dbsize_basic(mini_redis):

    assert mini_redis.dbsize() == 0


def test_incr_basic(mini_redis):

    assert mini_redis.incr('mutants') == 'OK'


def test_zadd_basic(mini_redis):

    assert mini_redis.zadd('mutants', 0, 0) == 1


def test_zcard_basic(mini_redis):

    assert mini_redis.zcard('mutants') == 0


def test_zrank_basic(mini_redis):

    assert mini_redis.zrank('mutants', 'four') is None


def test_zrange_basic(mini_redis):

    assert mini_redis.zrange('mutants', 0, 0) == []


# With Interactions


def test_get_existing_key(mini_redis_with_mutants):

    assert mini_redis_with_mutants.get('x1') == 'Wolverine'


def test_set_existing_key(mini_redis_with_mutants):

    assert mini_redis_with_mutants.get('x1') == 'Wolverine'

    mini_redis_with_mutants.set('x1', 'Xavier')

    assert mini_redis_with_mutants.get('x1') == 'Xavier'


def test_delete_result(mini_redis_with_mutants):
    assert mini_redis_with_mutants.get('x2') == 'Gambit'

    mini_redis_with_mutants.delete('x2')

    assert mini_redis_with_mutants.get('x2') is None


def test_delete_zkeys(mini_redis_with_ordered_mutants):
    mini_redis_with_ordered_mutants.delete('mutants')

    assert mini_redis_with_ordered_mutants.zrange('mutants', 0, -1) == []


def test_get_basic_key_in_ordered_set(mini_redis_with_ordered_mutants):

    with pytest.raises(CommandError):
        mini_redis_with_ordered_mutants.get('mutants')


def test_dbsize_only_keys(mini_redis_with_mutants):

    assert mini_redis_with_mutants.dbsize() == 3


def test_dbsize_with_zkeys(mini_redis_with_ordered_mutants):

    assert mini_redis_with_ordered_mutants.dbsize() == 1


def test_dbsize_with_keys_and_zkeys(mini_redis_with_all_mutants):

    assert mini_redis_with_all_mutants.dbsize() == 4


def test_incr_no_key(mini_redis):
    mini_redis.incr('mutants')

    assert mini_redis.get('mutants') == 1


def test_incr_valid_existing_key(mini_redis):
    mini_redis.set('mutants', 7)
    mini_redis.incr('mutants')

    assert mini_redis.get('mutants') == 8


def test_incr_invalid_case(mini_redis):
    mini_redis.set('mutant_houses', {'id': 2})

    with pytest.raises(CommandError):
        mini_redis.incr('mutant_houses')


def test_zcard(mini_redis):
    mini_redis.zadd('mutants', 1, 'uno')
    mini_redis.zadd('mutants', 2, 'two')

    assert mini_redis.zcard('mutants') == 2


def test_zrank_with_cases(mini_redis):
    mini_redis.zadd('mutants', 1, 'uno')
    mini_redis.zadd('mutants', 2, 'two')
    mini_redis.zadd('mutants', 3, 'three')

    assert mini_redis.zrank('mutants', 'three') == 2


def test_zrange_start_gt_stop(mini_redis):

    assert mini_redis.zrange('key', 2, 1) == []


def test_zrange_start_gt_len(mini_redis):
    mini_redis.zadd('mutants', 1, 'uno')

    assert mini_redis.zrange('mutants', 2, 1) == []


def test_zrange_with_all_values(mini_redis_with_ordered_mutants):

    assert mini_redis_with_ordered_mutants.zrange('mutants', 0, -1) == [
        'Wolverine',
        'Guepardo',
        'Gambit',
        'Quicksilver'
    ]


def test_zadd_different_index(mini_redis):
    mini_redis.zadd('mutants', 7, 'Cyclop')

    assert mini_redis.zrange('mutants', 0, 0) == ['Cyclop']


def test_zadd_with_elements(mini_redis_with_ordered_mutants):

    mini_redis_with_ordered_mutants.zadd('mutants', 0, 'Beast')

    assert mini_redis_with_ordered_mutants.zrange('mutants', 0, -1) == [
        'Beast',
        'Wolverine',
        'Guepardo',
        'Gambit',
        'Quicksilver'
    ]


def test_zrange_with_intermediate(mini_redis_with_ordered_mutants):

    assert mini_redis_with_ordered_mutants.zrange('mutants', 2, 3) == [
        'Gambit',
        'Quicksilver'
    ]
