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


def test_create_user_get_route(client):
    response = client.get('/create_user')
    assert b'Create new user:' in response.data


def test_create_user_when_user_doesnt_exist(client):
    response = client.post('/create_user', data=dict(
        name='david',
        email='david@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'david' in response.data


def test_create_user_when_name_is_duplicate(client):
    response = client.post('/create_user', data=dict(
        name='test_user_1',
        email='david@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'Duplicate user name!' in response.data


def test_create_user_when_email_is_duplicate(client):
    response = client.post('/create_user', data=dict(
        name='david',
        email='test_1@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'Duplicate email!' in response.data


def test_create_user_when_password_and_confirm_dont_match(client):
    response = client.post('/create_user', data=dict(
        name='david',
        email='david@email.com',
        password='pas123',
        confirm_password='pas1234'
        ), follow_redirects=True)
    assert b'Passwords do not match' in response.data


def test_edit_user_get_route(client):
    response = client.get('/edit_user/3')
    assert b'test_user_2' in response.data


def test_edit_user_with_valid_data(client):
    response = client.post('/edit_user/3', data=dict(
        user_id='3',
        name='test_user22',
        email='test_1@email.com',
        password='test1',
        confirm_password='test1'
        ), follow_redirects=True)
    assert b'test_user22' in response.data


def test_edit_user_with_duplicate_email(client):
    response = client.post('/edit_user/3', data=dict(
        user_id='3',
        name='test_user22',
        email='admin@email.com',
        password='test1',
        confirm_password='test1'
        ), follow_redirects=True)
    assert b'Duplicate email!' in response.data