import abc


class ImageRepositoryInterface(abc.ABC):
    """interface for image manipulation"""

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'add') and
                callable(subclass.add) and
                hasattr(subclass, 'update') and
                callable(subclass.update) and
                hasattr(subclass, 'delete') and
                callable(subclass.delete)  or
                NotImplemented)

    @abc.abstractmethod
    def add(self, image, post):
        pass

    @abc.abstractmethod
    def update(self, image, post):
        pass

    @abc.abstractmethod
    def delete(self, image_name):
        pass
