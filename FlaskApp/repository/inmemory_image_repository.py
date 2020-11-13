import base64
from repository.image_repository_interface import ImageRepositoryInterface


class InMemoryImageRepository(ImageRepositoryInterface):
    def __init__(self):
        pass

    def add(self, image, post):
        img = image.read()
        img = base64.b64encode(img).decode('ascii')
        post.image = "data:image/png;base64, " + img

    def update(self, image, post):
        self.add(image, post)

    def delete(self, image_name):
        pass
