# coding: utf-8

from __future__ import absolute_import
import six


class Message(object):
    """ see: https://api.slack.com/events/message
    """
    def __init__(self, message):
        params = message.copy()
        for k, v in six.iteritems(params):
            self.__dict__[k] = v

    def __getattr__(self, k):
        if not self.__dict__.get(k):
            return None
        return self.__dict__.get(k)

