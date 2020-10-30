from datetime import datetime


class User:
    """contains user properties"""

    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.created_at = datetime.now()
        self.modified_at = self.created_at
