# coding: utf-8
from __future__ import absolute_import, division
import json
import time
import warnings
import sys
import os
import datetime
import six
from .requests import Requests, HttpForbidden, Auth
from .rest import FromUrl

__all__ = ('Slack',)


_http_errors = {}


def jsonify(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    elif isinstance(obj, set):
        return list(obj)
    else:
        raise TypeError("Can't JSONify objects of type %s" % type(obj).__name__)


class _requests(Requests):
    def __init__(self, *p, **kw):
        super(_requests, self).__init__(*p, **kw)
        self.rl_remaining = 99999
        self.rl_reset = 0
        self.dump_reqs = '__SLACK_DEBUG_REQUESTS__' in os.environ

    @staticmethod
    def _data(data, kwargs):
        if isinstance(data, six.string_types):
            return data
        elif data is not None:
            kwargs.setdefault('headers',{})['Content-Type'] = 'application/json'
            rv = json.dumps(data, default=jsonify)
            return rv

    def _rl_sleep(self, until):
        t = until - time.time()
        if t > 0:
            warnings.warn("Slack has been rate limited; Waiting %0.1fs for the next reset." % t, Warning)
            time.sleep(t)

    def request(self, method, url, **kwargs):
        if self.dump_reqs:
            print >> sys.stderr, "REQUEST", method, url
        while True:
            try:
                if self.rl_remaining <= 0:
                    self._rl_sleep(self.rl_reset)
                resp = super(_requests, self).request(method, url, **kwargs)
            except HttpForbidden:
                e = sys.exc_info()[1]
                if e.response.json()['error'] == u'rate_limited':
                    self.rl_remaining = int(e.response.headers['Retry-After'])
                    self.rl_reset = float(e.response.headers['Retry-After'])
                    continue
                else:
                    raise
            return resp

    def post(self, url, data=None, **kwargs):
        data = self._data(data, kwargs)
        return super(_requests, self).post(url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        data = self._data(data, kwargs)
        return super(_requests, self).patch(url, data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        data = self._data(data, kwargs)
        return super(_requests, self).put(url, data=data, **kwargs)


class Slack(object):
    def __init__(self, token):
        self._requests = _requests(auth=Auth)

    def fromurl(self, url, **kwargs):
        return FromUrl(url, _requests=self._requests)(**kwargs)

    def get_room(self, name, **kwargs):
        kwargs.update({'name': name})   # TODO: Not smart?
        return self.fromurl('https://slack.com/api/channels.join', **kwargs)

    def apitest(self):
        return self.fromurl('https://slack.com/api/api.test', pretty=1)
