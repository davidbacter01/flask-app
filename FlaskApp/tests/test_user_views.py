

def test_create_user_get_route(client):
    response = client.get('/users/new')
    assert b'Create new user:' in response.data


def test_create_user_get_with_unconfigured_client(unconfigured_client):
    response = unconfigured_client.get('/users/new', follow_redirects=True)
    assert b'Database Setup' in response.data


def test_create_user_when_user_doesnt_exist(client):
    response = client.post('/users/new', data=dict(
        name='david',
        email='david@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'david' in response.data


def test_create_user_when_user_doesnt_exist_with_unconfigured_client(unconfigured_client):
    response = unconfigured_client.post('/users/new', data=dict(
        name='david',
        email='david@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_create_user_when_name_is_duplicate(client):
    response = client.post('/users/new', data=dict(
        name='test_user_1',
        email='david@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'Duplicate user name!' in response.data


def test_create_user_when_name_is_duplicate_with_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/users/new', data=dict(
        name='test_user_1',
        email='david@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_create_user_when_email_is_duplicate(client):
    response = client.post('/users/new', data=dict(
        name='david',
        email='test_1@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'Duplicate email!' in response.data


def test_create_user_when_email_is_duplicate_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/users/new', data=dict(
        name='david',
        email='test_1@email.com',
        password='pas123',
        confirm_password='pas123'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_create_user_when_password_and_confirm_dont_match(client):
    response = client.post('/users/new', data=dict(
        name='david',
        email='david@email.com',
        password='pas123',
        confirm_password='pas1234'
        ), follow_redirects=True)
    assert b'Passwords do not match' in response.data


def test_create_user_when_password_and_confirm_dont_match_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/users/new', data=dict(
        name='david',
        email='david@email.com',
        password='pas123',
        confirm_password='pas1234'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_edit_user_get_route(client):
    response = client.get('/users/edit/3')
    assert b'test_user_2' in response.data


def test_edit_user_get_route_unconfigured(unconfigured_client):
    response = unconfigured_client.get('/users/edit/3', follow_redirects=True)
    assert b'Database Setup' in response.data


def test_edit_user_with_valid_data(client):
    response = client.post('/users/edit/3', data=dict(
        user_id='3',
        name='test_user22',
        email='test_1@email.com',
        password='test1',
        confirm_password='test1'
        ), follow_redirects=True)
    assert b'test_user22' in response.data


def test_edit_user_with_valid_data_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/users/edit/3', data=dict(
        user_id='3',
        name='test_user22',
        email='test_1@email.com',
        password='test1',
        confirm_password='test1'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_edit_user_with_duplicate_email(client):
    response = client.post('/users/edit/3', data=dict(
        user_id='3',
        name='test_user22',
        email='admin@email.com',
        password='test1',
        confirm_password='test1'
        ), follow_redirects=True)
    assert b'Duplicate email!' in response.data


def test_edit_user_with_duplicate_email_unconfigured(unconfigured_client):
    response = unconfigured_client.post('/users/edit/3', data=dict(
        user_id='3',
        name='test_user22',
        email='admin@email.com',
        password='test1',
        confirm_password='test1'
        ), follow_redirects=True)
    assert b'Database Setup' in response.data


def test_delete_user(client):
    response = client.get('/users/delete/4')
    assert b'deleted' not in response.data


def test_delete_user_unconfigured(unconfigured_client):
    response = unconfigured_client.get('/users/delete/4', follow_redirects=True)
    assert b'deleted' not in response.data
