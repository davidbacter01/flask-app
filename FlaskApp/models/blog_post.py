from datetime import datetime


class BlogPost:
    def __init__(self, title: str, contents: str,
                 owner):
        self.blog_id = None
        self.title = title
        self.contents = contents
        self.owner = owner
        self.created_at = self.modified_at = datetime.now()
