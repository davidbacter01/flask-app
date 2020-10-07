from unittest.mock import Mock
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from setup.database import Database
from setup.config import Config


class Services:
    posts = 'posts'
    config = 'config'
    TESTING = False
    configuration = Config()
    db = Database(configuration)

    testing_services = {
        posts:InMemoryPostsRepository(),
        config:Mock()
        }

    production_services = {
        posts:DatabasePostsRepository(db),
        config:configuration
        }


    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]

        return Services.production_services[service_name]
