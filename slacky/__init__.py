# coding: utf-8
from __future__ import absolute_import, print_function
import json
import time
import warnings
import sys
import os
import datetime
import six
from .requests import Requests, HttpForbidden
from .rest import FromUrl

__all__ = ('Slacky',)


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
            print("REQUEST", method, url, file=sys.stderr)
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


class Slacky(object):
    def __init__(self, token):
        self._requests = _requests()
        self.token = token

    def fromurl(self, url, **kwargs):
        return FromUrl(url, _requests=self._requests)(**kwargs)

    @property
    def api(self):
        return self.fromurl('https://slack.com/api')

    @property
    def auth(self):
        return self.fromurl('https://slack.com/api/auth', token=self.token)

    @property
    def channels(self):
        return self.fromurl('https://slack.com/api/channels', token=self.token)

    @property
    def chat(self):
        return self.fromurl('https://slack.com/api/chat', token=self.token)

    @property
    def emoji(self):
        return self.fromurl('https://slack.com/api/emoji', token=self.token)

    @property
    def files(self):
        return self.fromurl('https://slack.com/api/files', token=self.token)

    @property
    def groups(self):
        return self.fromurl('https://slack.com/api/groups', token=self.token)

    @property
    def im(self):
        return self.fromurl('https://slack.com/api/im', token=self.token)

    @property
    def oauth(self):
        return self.fromurl('https://slack.com/api/oauth', token=self.token)

    @property
    def presence(self):
        return self.fromurl('https://slack.com/api/presence', token=self.token)

    @property
    def rtm(self):
        return self.fromurl('https://slack.com/api/rtm', token=self.token)

    @property
    def search(self):
        return self.fromurl('https://slack.com/api/search', token=self.token)

    @property
    def stars(self):
        return self.fromurl('https://slack.com/api/stars', token=self.token)

    @property
    def users(self):
        return self.fromurl('https://slack.com/api/users', token=self.token)

    def timeline(self, channel_name='general', count=16):
        result = []
        messages = self.channels.timeline(channel_name, count=count)
        for message in messages:
            result.append("%10s: %s"%(
                    self.users.get_name_by_id(message.user),
                    message.text,
                    )
                )
        return result
