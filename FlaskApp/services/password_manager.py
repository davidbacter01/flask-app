from passlib.hash import sha256_crypt


class PasswordManager:

    @staticmethod
    def hash(password):
        hashed = sha256_crypt.hash(password)
        return hashed


    @staticmethod
    def verify(password, hashed_password):
        return sha256_crypt.verify(password, hashed_password)
