# coding: utf-8

from __future__ import absolute_import
import requests

class HttpClientError(requests.exceptions.HTTPError):
    """The 4xx class of http status code.
    """

_http_errors = {}

class HttpBadRequest(HttpClientError):
    """400 Bad Request
    """
_http_errors[400] = HttpBadRequest


class HttpUnauthorized(HttpClientError):
    """401 Unauthorized
    """
_http_errors[401] = HttpUnauthorized


class HttpPaymentRequired(HttpClientError):
    """402 Payment Required
    """
_http_errors[402] = HttpPaymentRequired


class HttpForbidden(HttpClientError):
    """403 Forbidden
    """
_http_errors[403] = HttpForbidden


class HttpNotFound(HttpClientError):
    """404 Not Found
    """
_http_errors[404] = HttpNotFound


class HttpMethodNotAllowed(HttpClientError):
    """405 Method Not Allowed
    """
_http_errors[405] = HttpMethodNotAllowed


class HttpNotAcceptable(HttpClientError):
    """406 Not Acceptable
    """
_http_errors[406] = HttpNotAcceptable


class HttpProxyAuthenticationRequired(HttpClientError):
    """407 Proxy Authentication Required
    """
_http_errors[407] = HttpProxyAuthenticationRequired


class HttpRequestTimeout(HttpClientError):
    """408 Request Timeout
    """
_http_errors[408] = HttpRequestTimeout


class HttpConflict(HttpClientError):
    """409 Conflict
    """
_http_errors[409] = HttpConflict


class HttpGone(HttpClientError):
    """410 Gone
    """
_http_errors[410] = HttpGone


class HttpLengthRequired(HttpClientError):
    """411 Length Required
    """
_http_errors[411] = HttpLengthRequired


class HttpPreconditionFailed(HttpClientError):
    """412 Precondition Failed
    """
_http_errors[412] = HttpPreconditionFailed


class HttpRequestEntityTooLarge(HttpClientError):
    """413 Request Entity Too Large
    """
_http_errors[413] = HttpRequestEntityTooLarge


class HttpRequestUriTooLong(HttpClientError):
    """414 Request-URI Too Long
    """
_http_errors[414] = HttpRequestUriTooLong


class HttpUnsupportedMediaType(HttpClientError):
    """415 Unsupported Media Type
    """
_http_errors[415] = HttpUnsupportedMediaType


class HttpRequestedRangeNotSatisfiable(HttpClientError):
    """416 Requested Range Not Satisfiable
    """
_http_errors[416] = HttpRequestedRangeNotSatisfiable


class HttpExpectationFailed(HttpClientError):
    """417 Expectation Failed
    """
_http_errors[417] = HttpExpectationFailed


class HttpTooManyRequests(HttpClientError):
    """429 Too Many Requests
    """
_http_errors[429] = HttpTooManyRequests


class HttpServerError(requests.exceptions.HTTPError):
    """Server Error 5xx
    """


class HttpInternalServerError(HttpServerError):
    """500 Internal Server Error
    """
_http_errors[500] = HttpInternalServerError


class HttpNotImplemented(HttpServerError, NotImplementedError):
    """501 Not Implemented
    """
_http_errors[501] = HttpNotImplemented


class HttpBadGateway(HttpServerError):
    """502 Bad Gateway
    """
_http_errors[502] = HttpBadGateway


class HttpServiceUnavailable(HttpServerError):
    """503 Service Unavailable
    """
_http_errors[503] = HttpServiceUnavailable


class HttpGatewayTimeout(HttpServerError):
    """504 Gateway Timeout
    """
_http_errors[504] = HttpGatewayTimeout


class HttpVersionNotSupported(HttpServerError):
    """505 HTTP Version Not Supported
    """
_http_errors[505] = HttpVersionNotSupported


class Requests(requests.sessions.Session):
    def __init__(self, **kwargs):
        self._template = kwargs.copy()
        super(Requests, self).__init__()

    def _kw(self, kwargs):
        kw = self._template.copy()
        kw.update(kwargs)
        return kw

    def request(self, method, url, **kwargs):
        rv = super(Requests, self).request(method, url, **self._kw(kwargs))
        if rv.status_code in _http_errors:
            raise _http_errors[rv.status_code](rv.text, response=rv)
        rv.raise_for_status()
        return rv
