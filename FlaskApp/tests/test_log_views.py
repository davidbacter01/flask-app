import pytest
from app import application
from services.services import Services


@pytest.fixture
def client():
    Services.TESTING = True
    Services.get_service(Services.config).is_configured = True
    application.config['TESTING'] = True
    application.testing = True
    client = application.test_client()
    yield client


def test_login_route_get_method(client):
    response = client.get('/login')
    assert b'Login' in response.data


def test_login_route_post_method(client):
    response = client.post('/login', data=dict(
        user='admin',
        email='admin@email.com',
        password='secret'
        ), follow_redirects=True)

    assert b'Red flowers' in response.data


def test_login_failed(client):
    response = client.post('/login', data=dict(
        user='admin',
        email='admin@email.com',
        password='secrets'
        ), follow_redirects=True)

    assert b'Wrong password!' in response.data


def test_log_out(client):
    response = client.get('/logout', follow_redirects=True)
    assert b'Red flowers' in response.data