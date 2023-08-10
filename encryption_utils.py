from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import tkinter
from tkinter import simpledialog
import base64
import os

def derive_encryption_key(master_password):
    # Generate a random 16-byte salt
    salt = os.urandom(16)

    # Derive the encryption key using PBKDF2HMAC with SHA256
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key, salt

def decrypt_encrypted_key_with_salt_and_master_password(master_password, salt):
    # Derive the encryption key with the given salt and master password
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
    return key

def get_master_password():
    # Create a hidden root window to display the dialog
    root = tkinter.Tk()
    root.withdraw()

    # Prompt the user to enter the master password
    master_password = simpledialog.askstring("Master Password", "Enter your master password:")

    # Return the entered master password
    return master_password
