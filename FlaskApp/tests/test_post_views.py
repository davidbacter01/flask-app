import io
from tests.test_users_views import login_as_admin


def test_pagination_first_page(client):
    response = client.get('/?owner=All&page=1', follow_redirects=True)
    assert b'Next' in response.data
    assert b'Prev' not in response.data
    assert b'cactus' not in response.data


def test_pagination_second_page(client):
    response = client.get('/?owner=All&page=2', follow_redirects=True)
    assert b'Prev' in response.data
    assert b'Next' in response.data


def test_pagination_third_page(client):
    response = client.get('/?owner=All&page=3', follow_redirects=True)
    assert b'Prev' in response.data
    assert b'Next' not in response.data


def test_pagination_less_than_five_posts(client):
    response = client.get('/?owner=User1&page=1', follow_redirects=True)
    assert b'Prev' not in response.data
    assert b'Next' not in response.data


def test_index_route_with_filter(client):
    response = client.get('/?owner=User1', follow_redirects=True)
    assert b'random' not in response.data
    assert b'Red flowers' in response.data


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
        contents='test_contents',
        image=(io.BytesIO(b"some random data"), 'img.png')
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
    res = client.get('/view/1', follow_redirects=True)
    assert b'Red flowers' in res.data
    assert b'img' in res.data


def test_edit_post_when_not_logged_in(client):
    response = client.post('/edit/1', data=dict(
        title='Red flowers',
        contents='yes flowers'
    ), follow_redirects=True)
    assert b'Login' in response.data


def test_edit_post_when_logged_in_as_admin(client):
    login_as_admin(client)
    response = client.post('/edit/1', data=dict(
        title='Red flowers',
        contents='yes flowers',
        image=(io.BytesIO(b"some random data"), 'img.png')
    ), follow_redirects=True)
    assert b'yes flowers' in response.data


def test_edit_post_when_logged_in_as_owner(client):
    client.post('/login', data=dict(
        name='test_user_2',
        email='test_2@email.com',
        password='test2'
    ), follow_redirects=True)
    response = client.post('/edit/4', data=dict(
        title='edited title',
        contents='edited contents',
        image=(io.BytesIO(b"some random data"), 'img.png')
    ), follow_redirects=True)
    assert b'edited title' in response.data


def test_edit_post_when_logged_in_as_other_user(client):
    client.post('/login', data=dict(
        name='test_user_1',
        email='test_1@email.com',
        password='test1'
    ), follow_redirects=True)
    response = client.post('/edit/4', data=dict(
        title='edited title',
        contents='edited contents'
    ), follow_redirects=True)
    assert b'403' in response.data


def test_delete_post_not_logged_in(client):
    response = client.get('/delete/2', follow_redirects=True)
    assert b'Login' in response.data


def test_delete_post_logged_in_as_admin(client):
    login_as_admin(client)
    response = client.get('/delete/2', follow_redirects=True)
    assert b'Red flowers' in response.data
    assert b'Yellow flowers' not in response.data


def test_delete_post_when_logged_in_as_owner(client):
    client.post('/login', data=dict(
        name='test_user_2',
        email='test_2@email.com',
        password='test2'
    ), follow_redirects=True)
    response = client.get('/delete/5', follow_redirects=True)
    assert b'Red flowers' in response.data
    assert b'test delete' not in response.data


def test_delete_post_when_logged_in_as_different_user(client):
    client.post('/login', data=dict(
        name='test_user_1',
        email='test_1@email.com',
        password='test1'
    ), follow_redirects=True)
    response = client.get('/delete/4', follow_redirects=True)
    assert b'403' in response.data


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
