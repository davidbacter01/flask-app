class DatabaseSettings:
    """contains configuration details for database"""

    def __init__(self, db_name, user, password):
        self.section = 'postgres'
        self.host = 'localhost'
        self.user = user
        self.password = password
        self.db_name = db_name
