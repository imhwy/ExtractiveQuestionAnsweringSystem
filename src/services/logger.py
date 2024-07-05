"""
This module provides the QAsystem class which sets up logging for the question answering system.
"""
import os
import logging

LOG_NOTIFICATION = "====="


class QAsystem(object):
    """
    A class to handle logging for the question answering system.
    """
    def __init__(self,
                 file_name,
                 file_log="log",
                 write_to_file=False,
                 mode="info",
                 data_source='./log'):
        """
        Initialize the QAsystem instance.
        """
        self.file_name = file_name

        if not write_to_file:
            logging.basicConfig()

        self.logger = logging.getLogger(file_log)

        if write_to_file:
            hdlr = logging.FileHandler(os.path.join(
                data_source, '{}.log'.format(file_log)))
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s %(name)s %(message)s')
            hdlr.setFormatter(formatter)
            self.logger.addHandler(hdlr)

        self.logger.setLevel(logging.INFO)  # info, error

        if mode == "debug":
            self.logger.setLevel(logging.DEBUG)  # info, debug, error
            # self.logger.setLevel(logging.ERROR) # error

    def info(self, content):
        """
        Log an informational message.

        Args:
            content (str): The message content to log.
        """
        content = "{}:{}{}".format(self.file_name, LOG_NOTIFICATION, content)
        self.logger.info(content)

    def error(self, content):
        """
        Log an error message.

        Args:
            content (str): The message content to log.
        """
        content = "{}:{}{}".format(self.file_name, LOG_NOTIFICATION, content)
        self.logger.error(content)

    def debug(self, content):
        """
        Log a debug message.

        Args:
            content (str): The message content to log.
        """
        content = "{}:{}{}".format(self.file_name, LOG_NOTIFICATION, content)
        self.logger.debug(content)
