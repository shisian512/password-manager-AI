import sqlite3
import os
from base64 import urlsafe_b64encode, urlsafe_b64decode
from encryption import encrypt_password, decrypt_password

def create_sqlite_connection():
    conn = sqlite3.connect("password_manager.db")
    return conn

def save_password(account_name, password, encryption_key, account_description):
    encrypted_password = encrypt_password(password, encryption_key)
    try:
        conn = create_sqlite_connection()
        cursor = conn.cursor()

        # Insert the encrypted account name, password, and account description into the SQLite table
        query = "INSERT INTO passwords (account_name, encrypted_password, account_description) VALUES (?, ?, ?)"
        values = (account_name, encrypted_password, account_description)
        cursor.execute(query, values)

        conn.commit()
        cursor.close()

    except sqlite3.Error as err:
        print("Error:", err)

    finally:
        conn.close()

def get_available_ids():
    try:
        conn = create_sqlite_connection()
        cursor = conn.cursor()

        # Fetch all unique account_names from the passwords table
        query = "SELECT DISTINCT account_name FROM passwords"
        cursor.execute(query)

        available_ids = [row[0] for row in cursor.fetchall()]

        cursor.close()

        return available_ids

    except sqlite3.Error as err:
        print("Error:", err)

    finally:
        conn.close()

    # Return an empty list when there's an error or no data available
    return []

def get_password(account_name, encryption_key):
    try:
        conn = create_sqlite_connection()
        cursor = conn.cursor()

        # Fetch encrypted passwords for the given account_name from the passwords table
        query = "SELECT encrypted_password FROM passwords WHERE account_name = ?"
        values = (account_name,)
        cursor.execute(query, values)

        encrypted_passwords = [row[0] for row in cursor.fetchall()]

        cursor.close()

        # Decrypt the retrieved encrypted passwords
        decrypted_passwords = [decrypt_password(encrypted_password, encryption_key) for encrypted_password in encrypted_passwords]

        return decrypted_passwords

    except sqlite3.Error as err:
        print("Error:", err)

    finally:
        conn.close()

    return None

def delete_password(account_name, index):
    try:
        conn = create_sqlite_connection()
        cursor = conn.cursor()

        # Fetch encrypted passwords for the given account_name from the passwords table
        query = "SELECT encrypted_password FROM passwords WHERE account_name = ?"
        values = (account_name,)
        cursor.execute(query, values)

        encrypted_passwords = [row[0] for row in cursor.fetchall()]

        # Check if the index is valid
        if 0 <= index < len(encrypted_passwords):
            # Delete the password entry from the passwords table
            query = "DELETE FROM passwords WHERE account_name = ? AND encrypted_password = ?"
            values = (account_name, encrypted_passwords[index])
            cursor.execute(query, values)
            conn.commit()

        cursor.close()

    except sqlite3.Error as err:
        print("Error:", err)

    finally:
        conn.close()

def delete_all_passwords(encryption_key):
    try:
        conn = create_sqlite_connection()
        cursor = conn.cursor()

        # Delete all rows from the passwords table
        query = "DELETE FROM passwords"
        cursor.execute(query)
        conn.commit()

        cursor.close()

    except sqlite3.Error as err:
        print("Error:", err)

    finally:
        conn.close()

def create_table():
    conn = create_sqlite_connection()
    cursor = conn.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            account_name TEXT NOT NULL,
            encrypted_password TEXT NOT NULL,
            account_description TEXT
        )
    """
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()

def select_all_accounts():
    try:
        conn = create_sqlite_connection()
        cursor = conn.cursor()

        # Fetch all rows from the passwords table
        query = "SELECT * FROM passwords"
        cursor.execute(query)

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Fetch all rows and store them as dictionaries
        rows = []
        for row in cursor.fetchall():
            rows.append(dict(zip(column_names, row)))

        cursor.close()

        return rows

    except sqlite3.Error as err:
        print("Error:", err)

    finally:
        conn.close()

    return []