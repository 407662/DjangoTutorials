import logging


class UserFilter(logging.Filter):

    def filter(self, record):

        return '404' in record.getMessage() or '500' in record.getMessage()