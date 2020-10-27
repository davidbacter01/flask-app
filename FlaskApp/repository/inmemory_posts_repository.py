from models.blog_post import BlogPost
from repository.posts_repository_interface import PostsRepositoryInterface


class InMemoryPostsRepository(PostsRepositoryInterface):
    """implements CRUD operations"""
    def __init__(self):
        self.posts = [
            BlogPost('Red flowers', 'text about red flowers', 'User1'),
            BlogPost('Yellow flowers', 'text about yellow flowers', 'User2'),
            BlogPost('Blue flowers', 'text about blue flowers', 'User3'),
            BlogPost('test edit', 'random', 'test_user_2'),
            BlogPost('test delete', 'random', 'test_user_2'),
            BlogPost('Red flowers', 'text about red flowers', 'User1'),
            BlogPost('xyz', 'text about red flowers', 'User1'),
            BlogPost('abc12', 'text about red flowers', 8),
            BlogPost('ab', 'text about red flowers', 'are'),
            BlogPost('ab', 'text about red flowers', 'are'),
            BlogPost('ab', 'text about red flowers', 'are'),
            BlogPost('ab', 'text about red flowers', 'are')
            ]
        self.posts[0].blog_id = 1
        self.posts[1].blog_id = 2
        self.posts[2].blog_id = 3
        self.posts[3].blog_id = 4
        self.posts[4].blog_id = 5
        self.posts[5].blog_id = 6
        self.posts[6].blog_id = 7
        self.posts[7].blog_id = 8
        self.posts[8].blog_id = 9
        self.posts[9].blog_id = 10
        self.posts[10].blog_id = 11
        self.posts[11].blog_id = 12


    def count(self, user):
        if user in ('All', None):
            return len(self.posts)
        count = 0
        for post in self.posts:
            if post.owner == user:
                count += 1
        return count


    def get_by_id(self, post_id: int):
        '''returns a BlogPost object containing the provided post_id'''

        for post in self.posts:
            if post.blog_id == post_id:
                return post
        return None


    def get_all(self, owner, page_current):
        offset = (int(page_current) - 1) * 5
        if owner:
            posts = []
            for post in self.posts:
                if post.owner == owner:
                    posts.append(post)
            return posts[offset:5]
        return self.posts[offset:5]


    def add(self, post):
        post.blog_id = len(self.posts) + 1
        self.posts.insert(0, post)


    def remove(self, post_id):
        self.posts.remove(self.get_by_id(post_id))


    def edit(self, post):
        for blog_post in self.posts:
            if blog_post.blog_id == post.blog_id:
                blog_post = post
