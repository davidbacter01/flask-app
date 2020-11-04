from exceptions.exceptions import FileFormatError


class FileValidator:
    def __init__(self, extensions: list):
        """kwargs can be extensions=list"""
        self.extensions = extensions
        self.banned_names = ('', None)

    def validate_image(self, image):
        if not self.__has_name(image):
            raise FileFormatError('Image with no name provided!')
        if not self.__has_accepted_extensions(image):
            raise FileFormatError('File format is not suported!')

    def __has_name(self, image):
        return image.name not in self.banned_names

    def __has_accepted_extensions(self, image):
        name = image.filename
        if not "." in name:
            return False
        ext = name.rsplit(".", 1)[1]
        return ext.upper() in self.extensions
