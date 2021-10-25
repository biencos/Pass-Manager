from bcrypt import checkpw
from string import ascii_letters, digits, punctuation
from secrets import choice

from .aes import AESCipher

from ...database.manager import PasswordsDbManager


def decrypt_password(master_password, password):
    c = AESCipher(key=master_password)
    return c.decrypt(password)


def verify_master(username, master_password):
    db = PasswordsDbManager()
    hashed = db.get_user_master_password(username)
    if hashed:
        return checkpw(master_password.encode(), hashed.encode())
    return False


def encrypt_password(password, master_password):
    c = AESCipher(key=master_password)
    return c.encrypt(password)


def generate_password(length=8):
    alphabet = ascii_letters + digits + punctuation
    while True:
        password = ''.join(choice(alphabet) for i in range(length))
        if any(c.islower() for c in password) and any(c.isupper() for c in password) and any(c.isdigit() for c in password) and any(c in punctuation for c in password):
            break
    return password
