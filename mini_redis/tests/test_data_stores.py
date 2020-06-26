import pytest

from mini_redis.data_stores import SortedList


@pytest.fixture
def sorted_list():
    return SortedList()


@pytest.fixture
def sorted_list_with_mutants():
    sorted_list = SortedList()

    sorted_list.zadd(1, 'Wolverine')
    sorted_list.zadd(1, 'Guepardo')
    sorted_list.zadd(2, 'Gambit')
    sorted_list.zadd(3, 'Quicksilver')

    return sorted_list


def test_zcard_basic(sorted_list):

    assert sorted_list.zcard() == 0


def test_zcard_filled(sorted_list_with_mutants):

    assert sorted_list_with_mutants.zcard() == 4


def test_zcard_same_score(sorted_list):
    sorted_list.zadd(1, 'uno')
    sorted_list.zadd(1, 'two')
    sorted_list.zadd(1, 'three')

    assert sorted_list.zcard() == 3


def test_zrank_basic(sorted_list):

    assert sorted_list.zrank('Wolverine') is None


def test_zrank_filled(sorted_list_with_mutants):

    assert sorted_list_with_mutants.zrank('Wolverine') == 0


def test_zrange_start_gt_stop(sorted_list):

    assert sorted_list.zrange(2, 1) == []


def test_zrange_start_gt_len(sorted_list):
    sorted_list.zadd(1, 'uno')

    assert sorted_list.zrange(2, 1) == []


def test_zrange_with_all_values(sorted_list_with_mutants):

    assert sorted_list_with_mutants.zrange(0, -1) == [
        'Wolverine',
        'Guepardo',
        'Gambit',
        'Quicksilver'
    ]


def test_zadd_existing(sorted_list):
    sorted_list.zadd(1, 'Gambit')

    assert sorted_list.zadd(1, 'Gambit') == 0


def test_zadd_verify_float(sorted_list):
    sorted_list.zadd(1.2, 'Beast')
    sorted_list.zadd(1.0, 'Gambit')

    assert sorted_list.zrange(0, -1) == ['Gambit', 'Beast']


def test_zadd_different_index(sorted_list):
    sorted_list.zadd(7, 'Cyclop')

    assert sorted_list.zrange(0, 0) == ['Cyclop']


def test_zadd_with_elements(sorted_list_with_mutants):

    sorted_list_with_mutants.zadd(0, 'Beast')

    assert sorted_list_with_mutants.zrange(0, -1) == [
        'Beast',
        'Wolverine',
        'Guepardo',
        'Gambit',
        'Quicksilver'
    ]


def test_zrange_with_intermediate(sorted_list_with_mutants):

    assert sorted_list_with_mutants.zrange(2, 3) == [
        'Gambit',
        'Quicksilver'
    ]
