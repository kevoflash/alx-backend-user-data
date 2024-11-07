import logging
import re

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__()
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return re.sub(f';({|}'.join(map(re.escape, self.fields)) + ');', lambda m: self.REDACTION, message)
