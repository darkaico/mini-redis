"""
Note: following tests works as functionals because will call to MiniRedis implementation
"""
from mini_redis import MiniRedis


def test_get_key_no_value(api_client):
    response = api_client.get('/api/store/empty_key')
    data = response.json

    assert response.status_code == 200
    assert data['message']['value'] is None


def test_get_key_value(api_client):
    MiniRedis.instance().set('x1', 'Wolverine')
    response = api_client.get('/api/store/x1')
    data = response.json

    assert response.status_code == 200
    assert data['message']['value'] == 'Wolverine'


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
