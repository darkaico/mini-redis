from utils import data_utils


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


def test_is_float_valid():
    assert data_utils.is_float(2.2)


def test_is_float_valid_as_integer():
    assert data_utils.is_float(2)


def test_is_float_valid_str():
    assert data_utils.is_float('3.4')


def test_is_float_valid_str_as_integer():
    assert data_utils.is_float('5')


def test_is_float_negative_valid():
    assert data_utils.is_float(-9.9)


def test_is_float_negative_valid_as_integer():
    assert data_utils.is_float(-7)


def test_is_float_negative_valid_str():
    assert data_utils.is_float('-7.23')


def test_is_float_negative_valid_str_as_integer():
    assert data_utils.is_float('-89')


def test_is_float_invalid():
    assert not data_utils.is_float('G')


def test_is_float_invalid_none():
    assert not data_utils.is_float(None)
