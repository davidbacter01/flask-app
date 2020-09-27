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