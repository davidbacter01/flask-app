from unittest.mock import Mock
from repository.database_posts_repository import DatabasePostsRepository
from repository.inmemory_posts_repository import InMemoryPostsRepository
from setup.database import Database
from setup.dbconfig import DbConfig


class Services:
    posts = 'posts'
    config = 'config'
    TESTING = False
    db = Database(DbConfig())

    testing_services = {
        posts:InMemoryPostsRepository(),
        config:Mock()
        }

    production_services = {
        posts:DatabasePostsRepository(db),
        config:DbConfig()
        }


    @staticmethod
    def get_service(service_name):
        if Services.TESTING:
            return Services.testing_services[service_name]

        return Services.production_services[service_name]
