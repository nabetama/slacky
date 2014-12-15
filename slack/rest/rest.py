# coding: utf-8

from __future__ import absolute_import, division
import json
import re
import datetime
import dateutil.parser
import dateutil.tz
import six


_url_to_api_object = {}


class FromUrl(object):
    def __init__(self, url, _requests):
        self.url = url
        self._requests = _requests or __import__('requests')

    def __call__(self, **kwargs):
        for regix, klass in six.iteritems(_url_to_api_object):
            if regix.match(self.url):
                return klass(self, **kwargs)  # 自分自身を渡す
        raise NotImplementedError

    def get(self, **kwargs):
        self._requests.get(self.url, data=kwargs)

    def __repr__(self):
        return "<%s url=%r>" % (type(self).__name__, self.url)


class RestObject(object):
    def __init__(self, from_url, **kwargs):
        self.url = from_url.url
        self._requests = from_url._requests
        self.params = kwargs.copy()


# ================================================================================================
# Api
# ================================================================================================
class Api(RestObject):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/api.test', self._requests)()
_url_to_api_object[re.compile(r'^https://slack.com/api$')] = Api


class ApiTest(RestObject):
    def get(self, **kwargs):
        params = kwargs.copy()
        return self._requests.get(self.url, data=params)
_url_to_api_object[re.compile(r'^https://slack.com/api/api.test$')] = ApiTest


# ================================================================================================
# Auth
# ================================================================================================
class Auth(RestObject):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/auth.test', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/auth$')] = Auth


class AuthTest(RestObject):
    def post(self, **kwargs):
        return self._requests.request('POST', self.url, data=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/auth.test$')] = AuthTest

# ================================================================================================
# Channels
# ================================================================================================
class Channels(RestObject):
    def archive(self, channel):
        if not channel:
            print '[DEBUG] Input archive channel id.'
        self.params.update({'channel': channel})
        return FromUrl('https://slack.com/api/channels.archive', self._requests)(data=self.params)

    def create(self, name):
        if not name:
            print '[DEBUG] Input name for new channel.'
        self.params.update({'name': name})
        return FromUrl('https://slack.com/api/channels.create', self._requests)(data=self.params)

    def history(self, channel, **kwargs):
        """ https://api.slack.com/methods/channels.history
        latest, oldest, count
        """
        if not channel:
            print '[DEBUG] Please input the channel you\'d like to see.'
        self.params.update({'channel': channel})
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/channels.history', self._requests)(data=self.params)

    def info(self, channel):
        self.params.update({'channel': channel})
        return FromUrl('https://slack.com/api/channels.info', self._requests)(data=self.params)

    def invite(self, channel, user):
        self.params.update({
            'channel':  channel,
            'user':     user,
            })
        return FromUrl('https://slack.com/api/channels.invite', self._requests)(data=self.params)

    def join(self, channel):
        """ https://api.slack.com/methods/channels.join
        """
        self.params.update({
            'name': channel,
            })
        return FromUrl('https://slack.com/api/channels.join', self._requests)(data=self.params)

    def kick(self, channel, user):
        """ https://api.slack.com/methods/channels.kick
        """
        self.params.update({
            'channel':  channel,
            'user':     user,
            })
        return FromUrl('https://slack.com/api/channels.kick', self._requests)(data=self.params)

    def leave(self, channel):
        """ https://api.slack.com/methods/channels.leave
        """
        self.params.update({
            'channel':  channel,
            })
        return FromUrl('https://slack.com/api/channels.leave', self._requests)(data=self.params)

    @property
    def list(self):
        return FromUrl('https://slack.com/api/channels.list', self._requests)(data=self.params)

    def mark(self, channel, ts):
        """ https://api.slack.com/methods/channels.mark
        """
        self.params.update({
            'channel':  channel,
            'ts':       ts,
            })
        return FromUrl('https://slack.com/api/channels.mark', self._requests)(data=self.params)

    def rename(self, channel, new_name):
        """ https://api.slack.com/methods/channels.rename
        """
        self.params.update({
            'channel':  channel,
            'name':     new_name,
            })
        return FromUrl('https://slack.com/api/channels.rename', self._requests)(data=self.params)

    def set_purpose(self, channel, purpose):
        """ https://api.slack.com/methods/channels.setPurpose
        """
        self.params.update({
            'channel': channel,
            'purpose': purpose,
            })
        return FromUrl('https://slack.com/api/channels.setPurpose', self._requests)(data=self.params)

    def set_topic(self, channel, topic):
        """ https://api.slack.com/methods/channels.setTopic
        """
        self.params.update({
            'channel': channel,
            'topic': topic,
            })
        return FromUrl('https://slack.com/api/channels.setTopic', self._requests)(data=self.params)

    def unarchive(self, channel):
        """ https://api.slack.com/methods/channels.unarchive
        """
        self.params.update({
            'channel': channel,
            })
        return FromUrl('https://slack.com/api/channels.unarchive', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/channels$')] = Channels


class ChannelsArchive(RestObject):
    def post(self, **kwargs):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.archive$')] = ChannelsArchive


class ChannelsCreate(RestObject):
    def post(self, **kwargs):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.create$')] = ChannelsCreate


class ChannelsHistory(RestObject):
    def get(self, **kwargs):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.history$')] = ChannelsHistory


class ChannelsInfo(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.info$')] = ChannelsInfo


class ChannelsInvite(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.invite$')] = ChannelsInvite


class ChannelsJoin(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.join$')] = ChannelsJoin


class ChannelsKick(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.kick$')] = ChannelsKick


class ChannelsLeave(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.leave$')] = ChannelsLeave


class ChannelsList(RestObject):
    def get(self, **kwargs):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.list$')] = ChannelsList


class ChannelsLeave(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.leave$')] = ChannelsLeave


class ChannelsMark(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.mark$')] = ChannelsMark


class ChannelsRename(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.rename$')] = ChannelsRename


class ChannelsSetPurpose(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.setPurpose$')] = ChannelsSetPurpose


class ChannelsSetTopic(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.setTopic$')] = ChannelsSetTopic


class ChannelsUnarchive(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.unarchive$')] = ChannelsUnarchive


# ================================================================================================
# Chat
# ================================================================================================
class Chat(RestObject):
    def delete(self, channel, ts):
        """ https://api.slack.com/methods/chat.delete
        """
        self.params.update({
            'channel': channel,
            'ts':      ts,
            })
        return FromUrl('https://slack.com/api/chat.delete', self._requests)(data=self.params)

    def post_message(self, channel, text, **kwargs):
        """ https://api.slack.com/methods/chat.postMessage
        """
        self.params.update({
            'channel': channel,
            'text':    text,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/chat.postMessage', self._requests)(data=self.params)

    def update(self, channel, text, ts):
        """ https://api.slack.com/methods/chat.update
        """
        self.params.update({
            'channel': channel,
            'text':    text,
            'ts':      ts,
            })
        return FromUrl('https://slack.com/api/chat.update', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/chat$')] = Chat


class ChatDelete(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/chat.delete$')] = ChatDelete


class ChatPostMessage(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/chat.postMessage$')] = ChatPostMessage


class ChatUpdate(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/chat.update$')] = ChatUpdate


# ================================================================================================
# emoji
# ================================================================================================
class Emoji(RestObject):
    @property
    def list(self):
        return FromUrl('https://slack.com/api/emoji.list', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/emoji$')] = Emoji


class EmojiList(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/emoji.list$')] = EmojiList


# ================================================================================================
# file
# ================================================================================================
class Files(RestObject):
    def info(self, file, **kwargs):
        """ https://slack.com/api/files.info
        """
        self.params.update({
            'file': file,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/files.info', self._requests)(data=self.params)

    def list(self, **kwargs):
        """ https://api.slack.com/methods/files.list
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/files.list', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/files$')] = Files


class FilesInfo(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/files.info$')] = FilesInfo


class FilesList(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/files.list$')] = FilesList
