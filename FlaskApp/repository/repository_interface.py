import abc
from models.blog_post import BlogPost

class PostsRepositoryInterface(abc.ABC):
    """interface for posts manipulation"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'get_post_by_id') and 
                callable(subclass.get_post_by_id) and 
                hasattr(subclass, 'get_posts') and 
                callable(subclass.get_posts) and
                hasattr(subclass, 'add_post') and
                callable(subclass.add_post) and
                hasattr(subclass, 'remove_post') and
                callable(subclass.remove_post) and
                hasattr(subclass, 'edit_post') and
                callable(subclass.edit_post) or 
                NotImplemented)


    @abc.abstractmethod
    def get_post_by_id(self, post_id: int):
        pass


    @abc.abstractmethod
    def get_posts(self):
        pass


    @abc.abstractmethod
    def add_post(self, post:BlogPost):
        pass


    @abc.abstractmethod
    def remove_post(self, post_id):
        pass


    @abc.abstractmethod
    def edit_post(self, post:BlogPost):
        pass


