import hashlib
import getpass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

class Instrutor:
    def __init__(self, user_name, password_hash):
        self.user_name = user_name
        self.password_hash = password_hash
    



