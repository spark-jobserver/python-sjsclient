# -*- coding: utf-8 -*-


class SJSException(Exception):
    """The base exception class for all exceptions this library raises."""
    def __init__(self, message=None):
        self.message = self.__class__.__name__ if message is None else message
        super(Exception, self).__init__(self.message)


class HttpException(SJSException):
    def __init__(self, message, details=None, status_code=None):
        super(HttpException, self).__init__(message)
        self.details = details
        self.status_code = status_code

    def __unicode__(self):
        msg = self.__class__.__name__ + ": " + self.message
        if self.details:
            msg += ", " + self.details
        return msg

    def __str__(self):
        return self.__unicode__()


class NotFoundException(HttpException):
    """HTTP 404 Not Found."""
    pass
