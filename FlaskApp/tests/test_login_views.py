


def test_login_route_get_method(client):
    response = client.get('/login')
    assert b'Login' in response.data


def test_login_route_get_method_unconfigured(unconfigured_client):
    response = unconfigured_client.get('/login', follow_redirects=True)
    assert b'Database Setup' in response.data


def test_login_route_post_method(client):
    response = client.post('/login', data=dict(
        user='admin',
        email='admin@email.com',
        password='secret'
        ), follow_redirects=True)

    assert b'Red flowers' in response.data


def test_login_route_post_method_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/login', data=dict(
        user='admin',
        email='admin@email.com',
        password='secret'
        ), follow_redirects=True)

    assert b'Database Setup' in response.data


def test_login_failed(client):
    response = client.post('/login', data=dict(
        user='admin',
        email='admin@email.com',
        password='secrets'
        ), follow_redirects=True)

    assert b'Wrong password!' in response.data


def test_login_failed_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/login', data=dict(
        user='admin',
        email='admin@email.com',
        password='secrets'
        ), follow_redirects=True)

    assert b'Database Setup' in response.data


def test_log_out(client):
    response = client.get('/logout', follow_redirects=True)
    assert b'Red flowers' in response.data


def test_log_out_unconfigured(unconfigured_client):
    response = unconfigured_client.get('/logout', follow_redirects=True)
    assert b'Database Setup' in response.data
