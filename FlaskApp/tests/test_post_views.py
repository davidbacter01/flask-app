from tests.test_users_views import login_as_admin


def test_index_route(client):
    response = client.get('/index', follow_redirects=True)
    assert b'Red flowers' in response.data


def test_new_post_get_route(client):
    login_as_admin(client)
    response = client.get('/new', follow_redirects=True)
    assert b'Title' in response.data
    assert b'Content' in response.data


def test_new_post_get_route_when_not_logged_in(client):
    response = client.get('/new', follow_redirects=True)
    assert b'Log' in response.data


def test_new_post_post_route_when_logged(client):
    login_as_admin(client)
    response = client.post('/new', data=dict(
        title='test_title',
        contents='test_contents'
        ), follow_redirects=True)

    assert b'test_title' in response.data


def test_new_post_post_route_when_not_logged(client):
    response = client.post('/new', data=dict(
        title='test_title',
        contents='test_contents',
        owner='test_owner'
        ), follow_redirects=True)
    assert b'Login' in response.data


def test_view_post(client):
    assert b'Red flowers' in client.get('/view/1', follow_redirects=True).data


def test_edit_post_when_not_loged_in(client):
    response = client.post('/edit/1', data=dict(
        title='Red flowers',
        contents='yes flowers'
        ), follow_redirects=True)
    assert b'Login' in response.data


def test_edit_post_when_logged_in_as_admin(client):
    login_as_admin(client)
    response = client.post('/edit/1', data=dict(
        title='Red flowers',
        contents='yes flowers'
        ), follow_redirects=True)
    assert b'yes flowers' in response.data


def test_delete_post_not_logged_in(client):
    response = client.get('/delete/2', follow_redirects=True)
    assert b'Login' in response.data


def test_delete_post_logged_in_as_admin(client):
    login_as_admin(client)
    response = client.get('/delete/2', follow_redirects=True)
    assert b'Red flowers' in response.data
    assert b'Yellow flowers' not in response.data


def test_index_with_setup_not_configured(unconfigured_client):
    response = unconfigured_client.get('/', follow_redirects=True)
    assert b'Database Setup' in response.data


def test_new_post_get_route_with_unconfigured_client(unconfigured_client):
    response = unconfigured_client.get('/new', follow_redirects=True)
    assert b'Database Setup' in response.data


def test_view_post_with_unconfigured_client(unconfigured_client):
    response = unconfigured_client.get('/view/1', follow_redirects=True)
    assert b'Database Setup' in response.data


def test_edit_post_with_unconfigured_client(unconfigured_client):
    response = unconfigured_client.get('/edit/1', data=dict(
        title='something',
        contents='something'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_delete_post_with_unconfigured_client(unconfigured_client):
    response = unconfigured_client.get('/delete/1', follow_redirects=True)
    assert b'Database Setup' in response.data
