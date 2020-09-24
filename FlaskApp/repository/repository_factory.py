from repository.database_posts_repository import DatabasePostsRepository, PostsRepositoryInterface
from repository.posts_repository import PostsRepository


def repository_factory(production_condition) ->PostsRepositoryInterface:
    if production_condition:
        return DatabasePostsRepository("dbname=flask-app user=postgres password=postgres")

    return PostsRepository()
