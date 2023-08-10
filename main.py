import tkinter as tk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from password_storage import create_table
from interface import PasswordManagerApp
import login_system
import logging_config
from password_strength_predictor import word_char

# Create the database engine and session
engine = create_engine("sqlite:///password_manager.db", connect_args={'check_same_thread': True})
Session = sessionmaker(bind=engine)
Base = declarative_base()

if __name__ == "__main__":
    # Configure the logger
    logger = logging_config.configure_logging()
    logger.info("Application started")

    # Create the necessary table in the database if it doesn't exist
    create_table()

    # Perform the login process to get the encryption key and salt
    encryption_key, salt = login_system.login()

    # If the login was not successful, exit the application
    if not encryption_key:
        exit(1)

    # Create and configure the main Tkinter application window
    root = tk.Tk()
    root.attributes("-fullscreen", True)

    # Initialize and start the Password Manager application
    app = PasswordManagerApp(root, encryption_key, salt)
    root.mainloop()

    # The application has finished running
    logger.info("Application finished")
