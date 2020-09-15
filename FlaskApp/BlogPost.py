class BlogPost(object):
    
    def __init__(self, id, title, contents, owner, created_at, modified_at = ''):
        self.id = id
        self.title = title
        self.contents = contents
        self.owner = owner
        self.created_at = created_at
        self.modified_at = modified_at



