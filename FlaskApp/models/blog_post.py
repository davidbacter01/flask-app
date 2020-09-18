# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=too-few-public-methods
# pylint: disable=invalid-name
from datetime import datetime


class BlogPost:
    def __init__(self, blog_id: int, title: str, contents: str,
                owner: str):
        self.id = blog_id
        self.title = title
        self.contents = contents
        self.owner = owner
        self.created_at = datetime.now()
        self.modified_at = None
