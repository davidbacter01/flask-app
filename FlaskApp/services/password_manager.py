

class PasswordManager:

    def __init__(self, crypter):
        self.crypter = crypter


    def hash(self, password):
        hashed = self.crypter.hash(password)
        return hashed


    def verify(self, password, hashed_password):
        return self.crypter.verify(password, hashed_password)
