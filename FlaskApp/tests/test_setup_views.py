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


def test_db_setup(client):
    response = client.get('/setup')
    assert b'Database Setup' in response.data
