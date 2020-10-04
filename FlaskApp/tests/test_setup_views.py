import pytest
from app import application
from services.services import Services


@pytest.fixture
def client():
    Services.TESTING = True
    application.config['TESTING'] = True
    application.testing = True
    client = application.test_client()
    yield client


def test_db_setup(client):
    response = client.get('/setup')
    assert b'Database Setup' in response.data
