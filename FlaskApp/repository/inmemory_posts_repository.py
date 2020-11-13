import base64
from models.blog_post import BlogPost
from repository.posts_repository_interface import PostsRepositoryInterface


class InMemoryPostsRepository(PostsRepositoryInterface):
    """implements CRUD operations"""

    def __init__(self, users_repository=None, img_repo=None):
        self.img_repo = img_repo
        self.users = users_repository
        self.posts = [
            BlogPost('Red flowers', 'text about red flowers', 9),
            BlogPost('Yellow flowers', 'text about yellow flowers', 10),
            BlogPost('Blue flowers', 'text about blue flowers', 11),
            BlogPost('test edit', 'random', 12),
            BlogPost('test delete', 'random', 12),
            BlogPost('Red flowers', 'text about red flowers', 9),
            BlogPost('xyz', 'text about red flowers', 9),
            BlogPost('abc12', 'text about red flowers', 8),
            BlogPost('ab', 'text about red flowers', 13),
            BlogPost('ab', 'text about red flowers', 13),
            BlogPost('ab', 'text about red flowers', 13),
            BlogPost('cactus', 'text about red flowers', 13)
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
        self.__set_img()

    def count(self, user):
        if user in ('All', None):
            return len(self.posts)
        count = 0
        for post in self.posts:
            if post.owner == user:
                count += 1
        return count

    def get_by_id(self, post_id: int):
        """returns a BlogPost object containing the provided post_id"""
        for post in self.posts:
            if post.blog_id == post_id:
                return self.__get_post_with_true_owner(post)
        return None

    def get_all(self, owner, page_current):
        def get_id(post):
            return post.blog_id
        self.posts.sort(reverse=True, key=get_id)
        offset = (int(page_current) - 1) * 5
        last = offset + 5 if offset != 0 else 5
        posts = []
        if owner in ('All', None):
            for post in self.posts:
                posts.append(self.__get_post_with_true_owner(post))
            return posts[offset:last]
        for post in self.posts:
            for user in self.users.users:
                if user.user_id == post.owner:
                    if user.name == owner:
                        posts.append(self.__get_post_with_true_owner(post))
        return posts[offset:last]

    def add(self, post):
        post.blog_id = len(self.posts) + 1
        user = self.users.get_by_id(post.owner)
        self.img_repo.add(post.image, post)
        if user:
            self.posts.insert(0, post)

    def remove(self, post_id):
        for post in self.posts:
            if post.blog_id == post_id:
                self.posts.remove(post)
                break

    def edit(self, post):
        for blog_post in self.posts:
            if blog_post.blog_id == post.blog_id:
                self.posts.remove(blog_post)
                self.img_repo.update(post.image, post)
                self.posts.append(post)
                break

    def __get_post_with_true_owner(self, post: BlogPost):
        for user in self.users.users:
            if post.owner == user.user_id:
                updated_post = BlogPost(
                    post.title,
                    post.contents,
                    user.name
                )
                updated_post.blog_id = post.blog_id
                updated_post.created_at = post.created_at
                updated_post.modified_at = post.modified_at
                updated_post.image = post.image
                return updated_post
        return None

    def __set_img(self):
        for post in self.posts:
            post.image = '''data:image/png;base64,
            /9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkFBQoFBQU
            FBQ8ICQUKFBEWFhQRExMYHCggGBolGxMTITEhJSkrLi4uFx8zODMsNygtLi
            sBCgoKDQ0NDg0NFysdFRktKysrKystKysrKysrLSsrKysrLSs3KysrKysrK
            ysrKysrKysrKysrKysrKysrKysrK//AABEIAKgBLAMBIgACEQEDEQH/xAAV
            AAEBAAAAAAAAAAAAAAAAAAAABv/EABQQAQAAAAAAAAAAAAAAAAAAAAD/xAA
            WAQEBAQAAAAAAAAAAAAAAAAAABwb/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9
            oADAMBAAIRAxEAPwCMAZ9XwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAH//Z
            '''
