from __future__ import absolute_import, division
import json
import re
import datetime
import dateutil.parser
import dateutil.tz
import six


_url_to_api_object = {}


class Api(object):
    def __init__(self, url, _requests):
        self.url = url
        self._requests = _requests or __import__('requests')

    def __call__(self, **kwargs):
        params = {}
        if kwargs:
            merge_params = {}
            params.update(merge_params)
        text = self._requests.get(self.url, params=params).text
        return json.JSONDecoder().decode(text)

    def get(self, **kwargs):
        self._requests.get(self.url, data=kwargs)

    def __repr__(self):
        return "<%s url=%r>" % (type(self).__name__, self.url)


class RestObject(dict):
    @property
    def url(self):
        return self._requests.url

    def save(self):
        return self._requests.put(self.url, data=self).json()

    def delete(self):
        self._requests.delete(self.url)


class ApiTest(RestObject):
    def __init__(self, *p, **kw):
        super(ApiTest, self).__init__(*p, **kw)
_url_to_api_object[re.compile(r'^https://slack.com/api/api.test$')] = ApiTest
