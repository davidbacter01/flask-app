from repository.database_posts_repository import DatabasePostsRepository, PostsRepositoryInterface
from repository.inmemory_posts_repository import InMemoryPostsRepository


def posts_repository_factory(testing_condition=True) ->PostsRepositoryInterface:
    if not testing_condition:
        return DatabasePostsRepository("dbname=flask-app user=postgres password=postgres")

    return InMemoryPostsRepository()
