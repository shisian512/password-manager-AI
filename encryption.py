from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64

def encrypt_password(password, encryption_key):
    # Create a Fernet cipher suite using the provided encryption key
    cipher_suite = Fernet(encryption_key)

    # Encrypt the password using the Fernet cipher suite
    encrypted_password = cipher_suite.encrypt(password.encode())

    return encrypted_password

def decrypt_password(encrypted_password, encryption_key):
    # Create a Fernet cipher suite using the provided encryption key
    cipher_suite = Fernet(encryption_key)

    # Decrypt the encrypted password using the Fernet cipher suite
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()

    return decrypted_password