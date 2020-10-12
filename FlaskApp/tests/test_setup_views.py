

def test_db_setup(client):
    response = client.get('/setup')
    assert b'Database Setup' in response.data
