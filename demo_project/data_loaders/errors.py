from requests import HTTPError


class FreshdeskBaseError(HTTPError):
    """
    Base error class.
    Subclassing HTTPError to avoid breaking existing code that expects only HTTPErrors.
    """


class FreshdeskBadRequest(FreshdeskBaseError):
    """All the 40X and 501 status codes"""


class FreshdeskUnauthorized(FreshdeskBaseError):
    """401 Unauthorized"""


class FreshdeskAccessDenied(FreshdeskBaseError):
    """403 Forbidden"""


class FreshdeskNotFound(FreshdeskBaseError):
    """404 Error"""


class FreshdeskRateLimited(FreshdeskBaseError):
    """429 Rate Limit Reached"""


class FreshdeskServerError(FreshdeskBaseError):
    """50X errors"""
