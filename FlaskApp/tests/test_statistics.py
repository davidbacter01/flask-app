from tests.test_users_views import login_as_admin, login_as_test_user_2


def test_statistics_logged_in_as_admin(client):
    login_as_admin(client)
    response = client.get('/statistics/are', follow_redirects=True)
    assert b'4' in response.data
    assert b'are' in response.data

def test_statistics_not_logged(client):
    response = client.get('/statistics/are', follow_redirects=True)
    assert b'Login' in response.data

def test_statistics_logged_in_as_user(client):
    login_as_test_user_2(client)
    response = client.get('/statistics/are', follow_redirects=True)
    assert b'403' in response.data
