from mini_redis_server.mini_redis.utils import data_utils


def test_is_integer_valid():
    assert data_utils.is_integer(2)


def test_is_integer_valid_str():
    assert data_utils.is_integer('2')


def test_is_integer_negative_valid():
    assert data_utils.is_integer(-9)


def test_is_integer_negative_valid_str():
    assert data_utils.is_integer('-5')


def test_is_integer_invalid():
    assert not data_utils.is_integer('G')


def test_is_integer_invalid_none():
    assert not data_utils.is_integer(None)
