# pytest supports live logging so we have configured pytest.ini file to
# capture live log in common-tag-schema-logs.log file
# framework logs can be captured to the same aiops-logs.log file by using
# "create_file_logger" function.
# So logs are stored in common-tag-schema-logs-logs.log file are from both "create_file_logger"
# function and from live logging


import logging
import os
from datetime import datetime

from common_tag_schema import config

config_dir_path, logs_dir_path = config.create_directories()
now = datetime.now()
date_time = now.strftime("%Y-%-m-%d-%H%M%S")
file_name = logs_dir_path + 'common-tag-' + date_time + '.log'
file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)


def create_logger(logger_name=None):
    """
    :param logger_name:
    :return:
    """
    # create requested logger i.e creating a custom logger
    requested_logger = logging.getLogger(name=logger_name)
    return requested_logger


# def create_console_logger(logger=None):
#     """
#     :param logger:
#     :return:
#     I haven't used this function to capture the logs on console because
#     pytest live logging emits
#     logs to the console
#     """
#     logger.setLevel(logging.DEBUG)
#     # Create console handlers
#     console_handler = logging.StreamHandler()
#     # Create formatters and add it to handlers
#     console_formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     console_handler.setFormatter(console_formatter)
#     # Add handlers to the logger
#     logger.addHandler(console_handler)
#     return logger


def create_file_logger(logger=None):
    """
    :param logger:
    :return:
    """
    logger.setLevel(logging.DEBUG)
    # Create file handlers
    file_handler = logging.FileHandler(file_path)
    # Create formatters and add it to handlers
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    # Add handlers to the logger
    logger.addHandler(file_handler)
    return logger
