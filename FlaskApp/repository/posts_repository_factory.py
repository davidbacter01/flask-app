from repository.database_posts_repository import DatabasePostsRepository, PostsRepositoryInterface
from repository.inmemory_posts_repository import InMemoryPostsRepository


def posts_repository_factory(testing_condition) ->PostsRepositoryInterface:
    if not testing_condition:
        return DatabasePostsRepository()

    return InMemoryPostsRepository()
