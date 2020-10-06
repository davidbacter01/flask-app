from unittest.mock import Mock
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from setup.database import Database
from setup.config import Config


class Services:
    TESTING = False
    config = Config()
    db = Database(config)
    test_config = Mock()
    test_config.is_configured = True

    testing_services = {
        'posts':InMemoryPostsRepository(),
        'config':test_config
        }

    production_services = {
        'posts':DatabasePostsRepository(db),
        'config':config
        }


    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]

        return Services.production_services[service_name]
