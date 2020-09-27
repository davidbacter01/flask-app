import pytest
from app import application
from views import posts_views


@pytest.fixture
def client():
    application.config['TESTING'] = True
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
        title= 'test_title',
        contents= 'test_contents',
        owner= 'test_owner'
        ), follow_redirects=True)

    assert b'test_title' in response.data
    assert b'test_owner' in response.data


def test_view_post(client):
    assert b'text about red flowers' in client.get('/view/1').data
    assert b'text about yellow flowers' in client.get('/view/2').data
    assert b'text about blue flowers' in client.get('/view/3').data


def test_edit_post(client):
    response = client.post('/edit/1', data=dict(
        title='no flowers',
        contents='yes flowers'
        ), follow_redirects=True)
    assert b'no flowers' in response.data
    assert b'yes flowers' in response.data
    assert b'Red flowers' not in response.data


def test_delete_post(client):
    response = client.get('/delete/1')
    assert b'Red flowers' not in response.data

