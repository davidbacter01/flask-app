# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
class BlogPost:
    def __init__(self, blog_id: int, title: str, contents: str,
                owner: str, created_at, modified_at = ''):
        self.id = blog_id
        self.title = title
        self.contents = contents
        self.owner = owner
        self.created_at = created_at
        self.modified_at = modified_at
