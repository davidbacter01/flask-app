from models.blog_post import BlogPost
from repository.posts_repository_interface import PostsRepositoryInterface


class InMemoryPostsRepository(PostsRepositoryInterface):
    """implements CRUD operations"""
    def __init__(self):
        self.__posts = [
            BlogPost('Red flowers', 'text about red flowers', 'User1'),
            BlogPost('Yellow flowers', 'text about yellow flowers', 'User2'),
            BlogPost('Blue flowers', 'text about blue flowers', 'User3'),
            BlogPost('test edit', 'random', 'test_user_2'),
            BlogPost('test delete', 'random', 'test_user_2')
            ]
        self.__posts[0].blog_id = 1
        self.__posts[1].blog_id = 2
        self.__posts[2].blog_id = 3
        self.__posts[3].blog_id = 4
        self.__posts[4].blog_id = 5


    def get_by_id(self, post_id: int):
        '''returns a BlogPost object containing the provided post_id'''

        for post in self.__posts:
            if post.blog_id == post_id:
                return post
        return None


    def get_by_owner(self, owner):
        posts = []
        for post in self.__posts:
            if post.owner == owner:
                posts.append(post)
        return posts


    def get_all(self):
        return self.__posts


    def add(self, post):
        post.blog_id = len(self.__posts) + 1
        self.__posts.insert(0, post)


    def remove(self, post_id):
        self.__posts.remove(self.get_by_id(post_id))


    def edit(self, post):
        for blog_post in self.__posts:
            if blog_post.blog_id == post.blog_id:
                blog_post = post
