
def test_index(api_client):
    response = api_client.get('/')

    assert response.status_code == 200
