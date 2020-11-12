from tests.test_users_views import login_as_admin


def test_redirect_to_legacy_user_setup_on_first_login_attempt_for_old_user_not_setup(client):
    response = client.post('/login', data=dict(
        name='user',
        email='1',
        password='1'
        ), follow_redirects=True)
    assert b'You must complete user info before first login!' in response.data


def test_redirect_to_legacy_user_setup_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/login', data=dict(
        name='user',
        email='1',
        password='1'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_login_route_get_method(client):
    response = client.get('/login')
    assert b'Login' in response.data


def test_login_route_get_method_unconfigured(unconfigured_client):
    response = unconfigured_client.get('/login', follow_redirects=True)
    assert b'Database Setup' in response.data


def test_login_route_post_method(client):
    login_as_admin(client)
    client.post('/users/new', data=dict(
        name='abc',
        email='abc@email.com',
        password='123',
        confirm_password='123'
        ), follow_redirects=True)
    client.get('/logout')
    response = client.post('/login', data=dict(
        name='abc',
        email='abc@email.com',
        password='123'
        ), follow_redirects=True)

    assert b'cactus' in response.data


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

    assert b'Invalid username, email or password!' in response.data


def test_login_failed_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/login', data=dict(
        user='admin',
        email='admin@email.com',
        password='secrets'
        ), follow_redirects=True)

    assert b'Database Setup' in response.data


def test_log_out(client):
    response = client.get('/logout', follow_redirects=True)
    assert b'Login' in response.data


def test_log_out_unconfigured(unconfigured_client):
    response = unconfigured_client.get('/logout', follow_redirects=True)
    assert b'Database Setup' in response.data
