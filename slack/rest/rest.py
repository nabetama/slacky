# coding: utf-8

from __future__ import absolute_import, division
import json
import re
import six


_url_to_api_object = {}


class FromUrl(object):
    def __init__(self, url, _requests):
        self.url = url
        self._requests = _requests or __import__('requests')

    def __call__(self, **kwargs):
        try:
            for regix, klass in six.iteritems(_url_to_api_object):
                if regix.match(self.url):
                    return klass(self, **kwargs)  # 自分自身を渡す
            raise NotImplementedError
        except NotImplementedError as e:
            print regix.pattern, klass
            print  e

    def __repr__(self):
        return "<%s url=%r>" % (type(self).__name__, self.url)


class ApiBase(object):
    def __init__(self, from_url, **kwargs):
        self.url = from_url.url
        self._requests = from_url._requests
        self.params = kwargs.copy()


class RestObject(ApiBase):
    pass


# ================================================================================================
# Api
# ================================================================================================
class Api(ApiBase):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/api.test', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api$')] = Api


class ApiTest(RestObject):
    def get(self):
        return self._requests.get(self.url, data=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/api.test$')] = ApiTest


# ================================================================================================
# Auth
# ================================================================================================
class Auth(ApiBase):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/auth.test', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/auth$')] = Auth


class AuthTest(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/auth.test$')] = AuthTest

# ================================================================================================
# Channels
# ================================================================================================
class Channels(ApiBase):
    def get_channels(self, channel_name):
        channels = []
        for line in self.list.get().iter_lines():
            if line:
                channels = json.loads(line).get('channels')
        return channels

    def get_channel_id(self, channel_name):
        channels = self.get_channels(channel_name)
        for channel in channels:
            if channel['name'] == channel_name:
                return channel['id']
        return ''

    def archive(self, channel_name):
        channel_id = self.get_channel_id(channel_name)
        self.params.update({'channel': channel_id})
        return FromUrl('https://slack.com/api/channels.archive', self._requests)(data=self.params)

    def create(self, name):
        self.params.update({'name': name})
        return FromUrl('https://slack.com/api/channels.create', self._requests)(data=self.params)

    def history(self, channel_name, **kwargs):
        """ https://api.slack.com/methods/channels.history
        latest, oldest, count
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({'channel': channel_id})
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/channels.history', self._requests)(data=self.params)

    def info(self, channel_name):
        channel_id = self.get_channel_id(channel_name)
        self.params.update({'channel': channel_id})
        return FromUrl('https://slack.com/api/channels.info', self._requests)(data=self.params)

    def invite(self, channel_name, user):
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            'user':    user,
            })
        return FromUrl('https://slack.com/api/channels.invite', self._requests)(data=self.params)

    def join(self, channel_name):
        """ https://api.slack.com/methods/channels.join
        """
        self.params.update({
            'name': channel_name,
            })
        return FromUrl('https://slack.com/api/channels.join', self._requests)(data=self.params)

    def kick(self, channel_name, user):
        """ https://api.slack.com/methods/channels.kick
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            'user':     user,
            })
        return FromUrl('https://slack.com/api/channels.kick', self._requests)(data=self.params)

    def leave(self, channel_name):
        """ https://api.slack.com/methods/channels.leave
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            })
        return FromUrl('https://slack.com/api/channels.leave', self._requests)(data=self.params)

    @property
    def list(self):
        return FromUrl('https://slack.com/api/channels.list', self._requests)(data=self.params)

    def mark(self, channel_name, ts):
        """ https://api.slack.com/methods/channels.mark
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            'ts':       ts,
            })
        return FromUrl('https://slack.com/api/channels.mark', self._requests)(data=self.params)

    def rename(self, channel_name, new_name):
        """ https://api.slack.com/methods/channels.rename
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            'name':     new_name,
            })
        return FromUrl('https://slack.com/api/channels.rename', self._requests)(data=self.params)

    def set_purpose(self, channel_name, purpose):
        """ https://api.slack.com/methods/channels.setPurpose
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            'purpose': purpose,
            })
        return FromUrl('https://slack.com/api/channels.setPurpose', self._requests)(data=self.params)

    def set_topic(self, channel_name, topic):
        """ https://api.slack.com/methods/channels.setTopic
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            'topic': topic,
            })
        return FromUrl('https://slack.com/api/channels.setTopic', self._requests)(data=self.params)

    def unarchive(self, channel_name):
        """ https://api.slack.com/methods/channels.unarchive
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            })
        return FromUrl('https://slack.com/api/channels.unarchive', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/channels$')] = Channels


class ChannelsArchive(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.archive$')] = ChannelsArchive


class ChannelsCreate(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.create$')] = ChannelsCreate


class ChannelsHistory(RestObject):
    def get(self):
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
    def get(self):
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
class Chat(ApiBase):
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
class Emoji(ApiBase):
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
class Files(ApiBase):
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

    def upload(self, **kwargs):
        """ https://api.slack.com/methods/files.upload
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/files.upload', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/files$')] = Files


class FilesInfo(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/files.info$')] = FilesInfo


class FilesList(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/files.list$')] = FilesList


class FilesUpload(RestObject):
    def post(self):
        files = {}
        files = {'file': open(self.params['data']['file'])}
        return self._requests.post(self.url, params=self.params['data'], files=files)
_url_to_api_object[re.compile(r'^https://slack.com/api/files.upload$')] = FilesUpload


# ================================================================================================
# groups
# ================================================================================================
class Groups(ApiBase):
    def archive(self, channel):
        """ https://api.slack.com/methods/groups.archive
        """
        self.params.update({'channel': channel})
        return FromUrl('https://slack.com/api/groups.archive', self._requests)(data=self.params)

    def close(self, channel):
        """ https://api.slack.com/methods/groups.close
        """
        self.params.update({'channel': channel})
        return FromUrl('https://slack.com/api/groups.close', self._requests)(data=self.params)

    def create(self, name):
        """ https://api.slack.com/methods/groups.create
        """
        self.params.update({'channel': name})
        return FromUrl('https://slack.com/api/groups.create', self._requests)(data=self.params)

    def list(self, **kwargs):
        """ https://api.slack.com/methods/groups.list
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/groups.list', self._requests)(data=self.params)

    def create_child(self, channel):
        """ https://api.slack.com/methods/groups.createChild
        """
        self.params.update({'channel': channel})
        return FromUrl('https://slack.com/api/groups.createChild', self._requests)(data=self.params)

    def history(self, channel, **kwargs):
        """ https://api.slack.com/methods/groups.history
        """
        self.params.update({'channel': channel})
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/groups.history', self._requests)(data=self.params)

    def invite(self, channel, user):
        """ https://api.slack.com/methods/groups.invite
        """
        self.params.update({
            'channel': channel,
            'user':    user,
            })
        return FromUrl('https://slack.com/api/groups.invite', self._requests)(data=self.params)

    def kick(self, channel, user):
        """ https://api.slack.com/methods/groups.kick
        """
        self.params.update({
            'channel': channel,
            'user':    user,
            })
        return FromUrl('https://slack.com/api/groups.kick', self._requests)(data=self.params)

    def leave(self, channel):
        """ https://api.slack.com/methods/groups.leave
        """
        self.params.update({
            'channel': channel,
            })
        return FromUrl('https://slack.com/api/groups.leave', self._requests)(data=self.params)

    def mark(self, channel, ts):
        """ https://api.slack.com/methods/groups.mark
        """
        self.params.update({
            'channel': channel,
            'ts':      ts,
            })
        return FromUrl('https://slack.com/api/groups.mark', self._requests)(data=self.params)

    def open(self, channel):
        """ https://api.slack.com/methods/groups.open
        """
        self.params.update({
            'channel': channel,
            })
        return FromUrl('https://slack.com/api/groups.open', self._requests)(data=self.params)

    def rename(self, channel, new_name):
        """ https://api.slack.com/methods/groups.rename
        """
        self.params.update({
            'channel': channel,
            'name':    new_name,
            })
        return FromUrl('https://slack.com/api/groups.rename', self._requests)(data=self.params)

    def set_purpose(self, channel, purpose):
        """ https://api.slack.com/methods/groups.setPurpose
        """
        self.params.update({
            'channel': channel,
            'purpose': purpose,
            })
        return FromUrl('https://slack.com/api/groups.setPurpose', self._requests)(data=self.params)

    def set_topic(self, channel, topic):
        """ https://api.slack.com/methods/groups.setTopic
        """
        self.params.update({
            'channel': channel,
            'topic':   topic,
            })
        return FromUrl('https://slack.com/api/groups.setTopic', self._requests)(data=self.params)

    def unarchive(self, channel):
        """ https://api.slack.com/methods/groups.unarchive
        """
        self.params.update({
            'channel': channel,
            })
        return FromUrl('https://slack.com/api/groups.unarchive', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/groups$')] = Groups


class GroupsArchive(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.archive$')] = GroupsArchive


class GroupsList(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.list$')] = GroupsList


class GroupsClose(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.close$')] = GroupsClose


class GroupsCreate(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.create$')] = GroupsCreate


class GroupsCreateChild(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.createChild$')] = GroupsCreateChild


class GroupsHistory(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.history$')] = GroupsHistory


class GroupsInvite(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.invite$')] = GroupsInvite


class GroupsKick(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.kick$')] = GroupsKick


class GroupsLeave(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.leave$')] = GroupsLeave


class GroupsMark(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.mark$')] = GroupsMark


class GroupsOpen(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.open$')] = GroupsOpen


class GroupsRename(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.rename$')] = GroupsRename


class GroupsSetPurpose(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.setPurpose$')] = GroupsSetPurpose


class GroupsSetTopic(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.setTopic$')] = GroupsSetTopic


class GroupsUnarchive(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.unarchive$')] = GroupsUnarchive


# ================================================================================================
# im
# ================================================================================================
class Im(ApiBase):
    def list(self):
        """ https://api.slack.com/methods/im.list
        """
        return FromUrl('https://slack.com/api/im.list', self._requests)(data=self.params)

    def close(self, channel):
        """ https://api.slack.com/methods/im.close
        """
        self.params.update({
            'channel': channel,
            })
        return FromUrl('https://slack.com/api/im.close', self._requests)(data=self.params)

    def history(self, channel, **kwargs):
        """ https://api.slack.com/methods/im.history
        """
        self.params.update({
            'channel': channel,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/im.history', self._requests)(data=self.params)

    def mark(self, channel, ts):
        """ https://api.slack.com/methods/im.mark
        """
        self.params.update({
            'channel': channel,
            'ts':      ts,
            })
        return FromUrl('https://slack.com/api/im.mark', self._requests)(data=self.params)

    def open(self, user):
        """ https://api.slack.com/methods/im.history
        """
        self.params.update({
            'user': user,
            })
        return FromUrl('https://slack.com/api/im.open', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/im$')] = Im


class ImClose(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/im.close$')] = ImClose


class ImHistory(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/im.history$')] = ImHistory


class ImList(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/im.list$')] = ImList


class ImMark(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/im.mark$')] = ImMark


class ImOpen(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/im.open$')] = ImOpen


# ================================================================================================
# oauth
# ================================================================================================
class OAuth(ApiBase):
    def access(self, client_id, client_secret, code, **kwargs):
        """ https://api.slack.com/methods/oauth.access
        """
        self.params.update({
            'client_id':     client_id,
            'client_secret': client_secret,
            'code':          code,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/oauth.access', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/oauth$')] = OAuth


class OAuthAccess(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/oauth.access$')] = OAuth


# ================================================================================================
# presence
# ================================================================================================
class Presence(ApiBase):
    def set(self, presence):
        """ https://api.slack.com/methods/presence.set
        """
        self.params.update({
            'presence': presence,
            })
        return FromUrl('https://slack.com/api/presence.set', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/presence$')] = Presence


class PresenceSet(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/presence.set$')] = PresenceSet


# ================================================================================================
# rtm
# ================================================================================================
class Rtm(ApiBase):
    @property
    def start(self):
        """ https://api.slack.com/methods/rtm.start
        """
        return FromUrl('https://slack.com/api/rtm.start', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/rtm$')] = Rtm


class RtmStart(RestObject):
    """ https://api.slack.com/rtm
    """
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])

    def lasting(self, interval=1):
        # TODO: Return json per interval.
        import time
        while True:
            print self.get().json()
            time.sleep(interval)

_url_to_api_object[re.compile(r'^https://slack.com/api/rtm.start$')] = RtmStart


# ================================================================================================
# search
# ================================================================================================
class SearchBase(ApiBase):
    def search_from_url(self, query, **kwargs):
        if not self.url:
            raise AttributeError
        self.params.update({
            'query': query,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl(self.url, self._requests)(data=self.params)


class Search(SearchBase):
    def all(self, query, **kwargs):
        """ https://api.slack.com/methods/search.all
        """
        self.url = 'https://slack.com/api/search.all'
        return super(Search, self).search_from_url(query, **kwargs)

    def files(self, query, **kwargs):
        """ https://api.slack.com/methods/search.files
        """
        self.url = 'https://slack.com/api/search.files'
        return super(Search, self).search_from_url(query, **kwargs)

    def messages(self, query, **kwargs):
        """ https://api.slack.com/methods/search.messages
        """
        self.url = 'https://slack.com/api/search.messages'
        return super(Search, self).search_from_url(query, **kwargs)
_url_to_api_object[re.compile(r'^https://slack.com/api/search$')] = Search


class SearchAll(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/search.all$')] = SearchAll


class SearchFiles(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/search.files$')] = SearchFiles


class SearchMessages(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/search.messages$')] = SearchMessages


# ================================================================================================
# stars
# ================================================================================================
class Stars(ApiBase):
    def list(self, **kwargs):
        """ https://api.slack.com/methods/stars.list
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/stars.list', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/stars$')] = Stars


class StarsList(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/stars.list$')] = StarsList


# ================================================================================================
# users
# ================================================================================================
class Users(ApiBase):
    def info(self, user):
        """ https://api.slack.com/methods/users.info
        """
        self.params.update({
            'user': user,
            })
        return FromUrl('https://slack.com/api/users.info', self._requests)(data=self.params)

    @property
    def list(self):
        """ https://api.slack.com/methods/users.list
        """
        return FromUrl('https://slack.com/api/users.list', self._requests)(data=self.params)

    def set_active(self, user):
        """ https://api.slack.com/methods/users.setActive
        """
        self.params.update({
            'user': user,
            })
        return FromUrl('https://slack.com/api/users.setActive', self._requests)(data=self.params)
_url_to_api_object[re.compile(r'^https://slack.com/api/users$')] = Users


class UsersInfo(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/users.info$')] = UsersInfo


class UsersList(RestObject):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/users.list$')] = UsersList


class UsersSetActive(RestObject):
    def post(self):
        return self._requests.post(self.url, params=self.params['data'])
_url_to_api_object[re.compile(r'^https://slack.com/api/users.setActive$')] = UsersSetActive
