import os
from repository.image_repository_interface import ImageRepositoryInterface


class DiskImageRepository(ImageRepositoryInterface):
    def __init__(self, path):
        self.path = path

    def add(self, image, post):
        image.filename = str(post.id) + '.png'
        post.image = image.filename
        image.save(os.path.join(self.path, image.filename))

    def update(self, image, post):
        if post.image == 'default_blog.png':
            image.filename = str(post.id) + '.png'
        else:
            image.filename = '0'+ str(post.image)
        if os.path.exists(self.path + '/' + str(post.image))\
            and str(post.image) != 'default_blog.png':
            os.remove(self.path + '/' + str(post.image))
        post.image = image.filename
        image.save(os.path.join(self.path, image.filename))

    def delete(self, image_name):
        if os.path.exists(self.path + '/' + image_name)\
            and str(image_name) != 'default_blog.png':
            os.remove(self.path + '/' + image_name)
