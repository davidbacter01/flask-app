from models.blog_post import BlogPost
from repository.repository_interface import PostsRepositoryInterface

class PostsRepository(PostsRepositoryInterface):
    """implements CRUD operations"""
    def __init__(self):
        self.__posts = [
                BlogPost(1,'Red flowers', 'text about red flowers', 'User1'),
                BlogPost(2,'Yellow flowers', 'text about yellow flowers', 'User2'),
                BlogPost(3,'Blue flowers', 'text about blue flowers', 'User3')
                ]


    def get_post_by_id(self, post_id: int):
        for post in self.__posts:
            if post.id == post_id:
                return post

        return None


    def get_posts(self):
        return self.__posts


    def add_post(self, post):
        self.__posts.insert(0, post)


    def remove_post(self, post_id):
        self.__posts.remove(self.get_post_by_id(post_id))


    def edit_post(self, post):
        for blog_post in self.__posts:
            if blog_post.id == post.id:
                blog_post = post


#posts = PostsRepository()
