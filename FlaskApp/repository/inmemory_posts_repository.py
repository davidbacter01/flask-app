from models.blog_post import BlogPost
from repository.posts_repository_interface import PostsRepositoryInterface

class InMemoryPostsRepository(PostsRepositoryInterface):
    """implements CRUD operations"""
    def __init__(self):
        self.__posts = [
                BlogPost(1,'Red flowers', 'text about red flowers', 'User1'),
                BlogPost(2,'Yellow flowers', 'text about yellow flowers', 'User2'),
                BlogPost(3,'Blue flowers', 'text about blue flowers', 'User3')
                ]


    def get_by_id(self, post_id: int):
        '''returns a BlogPost object containing the provided post_id'''

        for post in self.__posts:
            if post.blog_id == post_id:
                return post

        return None


    def get_all(self):
        return self.__posts


    def add(self, post):
        self.__posts.insert(0, post)


    def remove(self, post_id):
        self.__posts.remove(self.get_by_id(post_id))


    def edit(self, post):
        for blog_post in self.__posts:
            if blog_post.blog_id == post.blog_id:
                blog_post = post


#posts = PostsRepository()
