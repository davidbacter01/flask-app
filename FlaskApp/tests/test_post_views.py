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

    print(response.data)
    assert b'test_title' in response.data
    assert b'test_owner' in response.data


