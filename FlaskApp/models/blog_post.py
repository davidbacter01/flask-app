from datetime import datetime


class BlogPost:
    def __init__(self, blog_id: int, title: str, contents: str,
                owner: str):
        self.blog_id = blog_id
        self.title = title
        self.contents = contents
        self.owner = owner
        self.created_at = self.modified_at = datetime.now()
