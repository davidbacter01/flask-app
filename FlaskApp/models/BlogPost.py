class BlogPost:   
    def __init__(self, id: int, title: str, contents: str, owner: str, created_at, modified_at = ''):
        self.id = id
        self.title = title
        self.contents = contents
        self.owner = owner
        self.created_at = created_at
        self.modified_at = modified_at
