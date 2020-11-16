def test_api_unconfigured(unconfigured_client):
    response = unconfigured_client.get("/api/post/10")
    assert b'Database Setup' in response.data

def test_api_configured_and_post_exists(client):
    response = client.get("/api/post/12")
    assert b'Red flowers' in response.data

def test_api_configured_post_doesnt_exist(client):
    response = client.get("/api/post/123")
    assert b'404' in response.data
