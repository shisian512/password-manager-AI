import secrets
import string
import logging
from password_strength_predictor import predict_password_strength, word_char

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a file handler and set the log file name
log_file = 'password_generator.log'
file_handler = logging.FileHandler(log_file)

# Add the file handler to the logger
logger.addHandler(file_handler)

def generate_password(length=12, use_digits=True, use_special=True):
    # Define the character set for generating passwords
    alphabet = string.ascii_letters
    if use_digits:
        alphabet += string.digits
    if use_special:
        alphabet += string.punctuation

    # Generate a random password of the specified length
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    # Predict the strength of the generated password
    strength = predict_password_strength(password)

    # Map the strength level to a descriptive string
    strength_str = "strong" if strength == 2 else "medium" if strength == 1 else "weak"

    # Log the generated password and its strength level
    logger.info(f"Generated password: {password}, Strength: {strength_str}")

    # If the strength is not strong enough (less than 2), generate a new password
    if strength < 2:
        logger.info(f"The strength of the password generated is {strength_str}.")
        logger.info(f"Generating a new password...")
        generate_password()

    return password