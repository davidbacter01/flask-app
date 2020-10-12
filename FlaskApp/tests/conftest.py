import pytest
from app import application
from services.services import Services


@pytest.fixture
def client():
    Services.TESTING = True
    application.config['TESTING'] = True
    application.testing = True
    Services.get_service(Services.config).is_configured = True
    client = application.test_client()
    yield client


@pytest.fixture
def unconfigured_client():
    Services.TESTING = True
    Services.get_service(Services.config).is_configured = False
    application.config['TESTING'] = True
    application.testing = True
    client = application.test_client()
    yield client
