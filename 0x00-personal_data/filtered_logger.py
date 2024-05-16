#!/usr/bin/env python3
"""
Write a function called filter_datum that
returns the log message obfuscated
"""

import re
from typing import List


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated
    """
    for field in fields:
        reg = f"{field}=[^{separator}]*"
        message = re.sub(reg, f"{field}={redaction}", message)
    return message
