#!/usr/bin/env python3
"""
Write a function called filter_datum that
returns the log message obfuscated
"""

import re
from typing import List
import logging
import mysql.connector
import os


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
        """init Doc"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format Doc"""
        original_msg = super().format(record)
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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name,
        auth_plugin='mysql_native_password'
    )


def main() -> None:
    """main function that takes no arguments
    and returns nothing.
    """
    database = get_db()
    cursor = database.cursor()
    cursor.execute("SELECT * FROM users;")
    log = get_logger()
    for row in cursor:
        data = []
        for des, val in zip(cursor.description, row):
            data.append(f"{des[0]}={str(val)}")
        rows = "; ".join(data)
        log.info(rows)
    cursor.close()
    database.close()


if __name__ == "__main__":
    """Main"""
    main()
