

def test_db_setup(client):
    response = client.get('/setup')
    assert b'405' in response.data
