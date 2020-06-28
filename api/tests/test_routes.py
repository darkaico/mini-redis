"""
Note: following tests works as functional tests
because will call to MiniRedis implementation and given its
Singleton threaded inheritance works in conjunction to all the tests.
"""
from mini_redis import MiniRedis


def test_get_key_no_value(api_client):
    response = api_client.get('/api/store/empty_key')
    data = response.json

    assert response.status_code == 200
    assert data['value'] is None


def test_get_key_value(api_client):
    MiniRedis.instance().set('x1', 'Wolverine')
    response = api_client.get('/api/store/x1')
    data = response.json

    assert response.status_code == 200
    assert data['value'] == 'Wolverine'


def test_wrong_store(api_client):
    MiniRedis.instance().zadd('avengers', 1, 'Captain America')
    response = api_client.get('/api/store/avengers')
    data = response.json

    assert response.status_code == 400
    assert data['error'] == 'Operation against a key holding the wrong kind of value'


def test_set_value(api_client):
    response = api_client.put('/api/store/x1', json={'value': 'Gambit'})
    data = response.json

    assert response.status_code == 200
    assert data['message'] == 'OK'
    assert MiniRedis.instance().get('x1') == 'Gambit'


def test_delete_key_no_value(api_client):
    response = api_client.delete('/api/store/x1')
    data = response.json

    assert response.status_code == 200
    assert data['message'] == 'OK'


def test_delete_key_with_value(api_client):
    MiniRedis.instance().set('x1', 'Wolverine')
    response = api_client.delete('/api/store/x1')
    data = response.json

    assert response.status_code == 200
    assert data['message'] == 'OK'
    assert MiniRedis.instance().get('x1') is None


def test_incr_no_value(api_client):
    response = api_client.put('/api/store/mutants/incr')
    data = response.json

    assert response.status_code == 200
    assert data['message'] == 'OK'
    assert MiniRedis.instance().get('mutants') == 1


def test_incr_with_value(api_client):
    MiniRedis.instance().set('mutants', 1)
    response = api_client.put('/api/store/mutants/incr')
    data = response.json

    assert response.status_code == 200
    assert data['message'] == 'OK'
    assert MiniRedis.instance().get('mutants') == 2


def test_incr_wrong_value(api_client):
    MiniRedis.instance().set('x1', 'Gambit')
    response = api_client.put('/api/store/x1/incr')
    data = response.json

    assert response.status_code == 400
    assert data['error'] == 'value is not an integer or out of range'


def test_zcard_no_value(api_client):
    response = api_client.get('/api/store/humans/zcard')
    data = response.json

    assert response.status_code == 200
    assert data['value'] == 0


def test_zcard_no_value(api_client):
    response = api_client.get('/api/store/humans/zcard')
    data = response.json

    assert response.status_code == 200
    assert data['value'] == 0


def test_zcard_wrong_store(api_client):
    MiniRedis.instance().set('first_class', 'active')
    response = api_client.get('/api/store/first_class/zcard')
    data = response.json

    assert response.status_code == 400
    assert data['error'] == 'Operation against a key holding the wrong kind of value'


def test_zcard_existing_value(api_client):

    MiniRedis.instance().zadd('aliens', 1, 'outlander_one')
    MiniRedis.instance().zadd('aliens', 2, 'outlander_two')

    response = api_client.get('/api/store/aliens/zcard')
    data = response.json

    assert response.status_code == 200
    assert data['value'] == 2


def test_zrank_no_value(api_client):
    response = api_client.get('/api/store/jedis/zrank/0')
    data = response.json

    assert response.status_code == 200
    assert data['value'] == None


def test_zrank_existing_value(api_client):

    MiniRedis.instance().zadd('jedis', 1, 'obi')
    MiniRedis.instance().zadd('jedis', 1, 'leia')
    MiniRedis.instance().zadd('jedis', 2, 'anakin')

    response = api_client.get('/api/store/jedis/zrank/anakin')
    data = response.json

    assert response.status_code == 200
    assert data['value'] == 2


def test_zadd_valid(api_client):
    response = api_client.put('/api/store/defenders/zadd', json={'score': 1, 'member': 'Daredevil'})
    data = response.json

    assert response.status_code == 200
    assert data['value'] == 1

    assert MiniRedis.instance().zrank('defenders', 'Daredevil') == 0


def test_zadd_invalid(api_client):
    response = api_client.put('/api/store/defenders/zadd', json={'score': "f", 'member': 'Daredevil'})
    data = response.json

    assert response.status_code == 400
    assert data['error'] == 'value is not a valid float'


def test_zrange_missing_attributes(api_client):
    response = api_client.get('/api/store/jedis/zrange')
    data = response.json

    assert response.status_code == 400
    assert data['error'] == 'value is not an integer or out of range'


def test_zrange_empty_attributes(api_client):
    response = api_client.get('/api/store/galactis/zrange?start=0&stop=0')
    data = response.json

    assert response.status_code == 200
    assert data['range'] == []


def test_zrange_existing_value(api_client):

    MiniRedis.instance().zadd('syths', 1, 'palpatine')
    MiniRedis.instance().zadd('syths', 1, 'kylo')
    MiniRedis.instance().zadd('syths', 2, 'anakin')

    response = api_client.get('/api/store/syths/zrange?start=0&stop=-1')
    data = response.json

    assert response.status_code == 200
    assert data['range'] == ['palpatine', 'kylo', 'anakin']
