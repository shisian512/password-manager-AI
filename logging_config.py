import logging

def configure_logging(log_file='app.log'):
    # Create a logger with the name 'app'
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)  # Set the logger's level to DEBUG

    # Create a formatter for log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler to write log messages to the specified log file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)  # Set the file handler's level to DEBUG
    file_handler.setFormatter(formatter)  # Set the formatter for the file handler

    # Create a stream handler to output log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set the console handler's level to INFO
    console_handler.setFormatter(formatter)  # Set the formatter for the console handler

    # Add the file handler and console handler to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
