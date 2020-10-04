import pytest
from app import application
from views.posts_views import TESTING


TESTING = True

@pytest.fixture
def client():
    application.config['TESTING'] = TESTING
    application.testing = True
    client = application.test_client()
    yield client


def test_index_route(client):
    response = client.get('/')
    assert b'Red flowers' in response.data


def test_new_post_get_route(client):
    response = client.get('/new')
    assert b'Title' in response.data
    assert b'Owner' in response.data
    assert b'Content' in response.data


def test_new_post_post_route(client):
    response = client.post('/new', data=dict(
        title='test_title',
        contents='test_contents',
        owner='test_owner'
        ), follow_redirects=True)

    assert b'test_title' in response.data
    assert b'test_owner' in response.data


def test_view_post(client):
    assert b'Red flowers' in client.get('/view/1').data


def test_edit_post(client):
    response = client.post('/edit/1', data=dict(
        title='Red flowers',
        contents='yes flowers'
        ), follow_redirects=True)
    assert b'yes flowers' in response.data
    assert b'text about red flowers' not in response.data


def test_delete_post(client):
    response = client.get('/delete/2')
    assert b'Yellow flowers' not in response.data
