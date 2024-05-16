#!/usr/bin/env python3
"""
Write a function called filter_datum that
returns the log message obfuscated
"""

import re
from typing import List
import logging


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    for field in fields:
        reg = f"{field}=[^{separator}]*"
        message = re.sub(reg, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        original_msg = logging.Formatter(self.FORMAT).format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_msg, self.SEPARATOR)


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def get_logger() -> logging.Logger:
    """
    Returns a logging object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_h = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_h.setFormatter(formatter)
    logger.addHandler(stream_h)
    return logger
