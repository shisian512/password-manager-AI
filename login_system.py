import os
import json
import time
import tkinter as tk
from tkinter import messagebox
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from encryption_utils import derive_encryption_key, get_master_password, decrypt_encrypted_key_with_salt_and_master_password

def save_key_and_salt_to_file(key, salt):
    # Save the encryption key and salt to a JSON file
    data = {
        "key": key.decode(),  # Convert bytes to string for JSON serialization
        "salt": salt.hex()    # Convert bytes to hex string for JSON serialization
    }
    with open("keyfile.json", "w") as file:
        json.dump(data, file)

def read_key_and_salt_from_file():
    # Read the encryption key and salt from the JSON file if it exists
    if os.path.exists("keyfile.json"):
        with open("keyfile.json", "r") as file:
            data = json.load(file)
            key = data["key"].encode()      # Convert string to bytes
            salt = bytes.fromhex(data["salt"])  # Convert hex string to bytes
            return key, salt
    return None, None

def login():
    # Perform the login process with a maximum number of attempts
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        master_password = get_master_password()
        key, salt = read_key_and_salt_from_file()

        if key and salt:
            # Derive the encryption key using the provided salt and master password
            derived_key = decrypt_encrypted_key_with_salt_and_master_password(master_password, salt)
            if key == derived_key:
                # Login successful, return the encryption key and salt
                return key, salt
        else:
            # First-time login, derive a new encryption key and save it
            derived_key, salt = derive_encryption_key(master_password)
            save_key_and_salt_to_file(derived_key, salt)
            messagebox.showinfo("Success", "First-time login successful.")
            return derived_key, salt

        # Invalid password, prompt user to try again
        messagebox.showerror("Error", "Invalid password. Please try again.")
        attempt += 1

    # Maximum login attempts reached, exit the application after a delay
    messagebox.showerror("Error", "Maximum login attempts reached. Quitting the application in 5 seconds.")
    time.sleep(5)
    exit(1)
