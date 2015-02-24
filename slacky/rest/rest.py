# coding: utf-8

from __future__ import absolute_import, print_function
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
                    return klass(self, **kwargs)
            raise NotImplementedError
        except NotImplementedError as e:
            print(e)
            print(regix.pattern, klass)

    def __repr__(self):
        return "<%s url=%r>" % (type(self).__name__, self.url)


class ApiBase(object):
    def __init__(self, from_url, **kwargs):
        self.url = from_url.url
        self._requests = from_url._requests
        self.params = kwargs.copy()


class RestObject(ApiBase):
    def get(self):
        return self._requests.get(self.url, params=self.params['data'])

    def post(self):
        return self._requests.post(self.url, params=self.params['data'])

# ================================================================================================
# Api
# ================================================================================================
class Api(ApiBase):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/api.test', self._requests)(data=self.params).get()
_url_to_api_object[re.compile(r'^https://slack.com/api$')] = Api


class ApiTest(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/api.test$')] = ApiTest


# ================================================================================================
# Auth
# ================================================================================================
class Auth(ApiBase):
    @property
    def test(self):
        return FromUrl('https://slack.com/api/auth.test', self._requests)(data=self.params).get()
_url_to_api_object[re.compile(r'^https://slack.com/api/auth$')] = Auth


class AuthTest(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/auth.test$')] = AuthTest

# ================================================================================================
# Channels
# ================================================================================================
class Channels(ApiBase):
    def all(self):
        channels = []
        for line in self.list.iter_lines():
            if line:    # JSON string.
                channels = json.loads(line).get('channels')
        return channels

    def get_channel_id(self, channel_name):
        for channel in self.all():
            if channel['name'] == channel_name:
                return channel['id']
        return ''

    def archive(self, channel_name):
        """ https://api.slack.com/methods/channels.archive
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({'channel': channel_id})
        return FromUrl('https://slack.com/api/channels.archive', self._requests)(data=self.params).post()

    def create(self, name):
        """ https://api.slack.com/methods/channels.create
        """
        self.params.update({'name': name})
        return FromUrl('https://slack.com/api/channels.create', self._requests)(data=self.params).post()

    def history(self, channel_name, **kwargs):
        """ https://api.slack.com/methods/channels.history
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({'channel': channel_id})
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/channels.history', self._requests)(data=self.params).get()

    def info(self, channel_name):
        """ https://api.slack.com/methods/channels.info
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({'channel': channel_id})
        return FromUrl('https://slack.com/api/channels.info', self._requests)(data=self.params).get()

    def invite(self, channel_name, user):
        """ https://api.slack.com/methods/channels.invite
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            'user':    user,
            })
        return FromUrl('https://slack.com/api/channels.invite', self._requests)(data=self.params).post()

    def join(self, channel_name):
        """ https://api.slack.com/methods/channels.join
        """
        self.params.update({
            'name': channel_name,
            })
        return FromUrl('https://slack.com/api/channels.join', self._requests)(data=self.params).post()

    def kick(self, channel_name, user):
        """ https://api.slack.com/methods/channels.kick
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            'user':     user,
            })
        return FromUrl('https://slack.com/api/channels.kick', self._requests)(data=self.params).post()

    def leave(self, channel_name):
        """ https://api.slack.com/methods/channels.leave
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            })
        return FromUrl('https://slack.com/api/channels.leave', self._requests)(data=self.params).post()

    @property
    def list(self):
        """ https://api.slack.com/methods/channels.list
        """
        return FromUrl('https://slack.com/api/channels.list', self._requests)(data=self.params).get()

    def mark(self, channel_name, ts):
        """ https://api.slack.com/methods/channels.mark
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            'ts':       ts,
            })
        return FromUrl('https://slack.com/api/channels.mark', self._requests)(data=self.params).post()

    def rename(self, channel_name, new_name):
        """ https://api.slack.com/methods/channels.rename
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel':  channel_id,
            'name':     new_name,
            })
        return FromUrl('https://slack.com/api/channels.rename', self._requests)(data=self.params).post()

    def set_purpose(self, channel_name, purpose):
        """ https://api.slack.com/methods/channels.setPurpose
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            'purpose': purpose,
            })
        return FromUrl('https://slack.com/api/channels.setPurpose', self._requests)(data=self.params).post()

    def set_topic(self, channel_name, topic):
        """ https://api.slack.com/methods/channels.setTopic
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            'topic': topic,
            })
        return FromUrl('https://slack.com/api/channels.setTopic', self._requests)(data=self.params).post()

    def unarchive(self, channel_name):
        """ https://api.slack.com/methods/channels.unarchive
        """
        channel_id = self.get_channel_id(channel_name)
        self.params.update({
            'channel': channel_id,
            })
        return FromUrl('https://slack.com/api/channels.unarchive', self._requests)(data=self.params).post()

    def timeline(self, channel_name, reverse=False, **kwargs):
        timeline = self.__timeline(channel_name, reverse, **kwargs)
        return timeline

    def __timeline(self, channel_name, is_reverse, **kwargs):
        from ..events import Message
        params   = {}
        messages = []
        if kwargs:
            self.params.update(kwargs)
        lines = self.history(channel_name, **params).json()['messages']
        lines = sorted(lines, key=lambda x: x['ts'], reverse=is_reverse)
        for line in lines:
            messages.append(Message(line))
        return messages
_url_to_api_object[re.compile(r'^https://slack.com/api/channels$')] = Channels


class ChannelsArchive(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.archive$')] = ChannelsArchive


class ChannelsCreate(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.create$')] = ChannelsCreate


class ChannelsHistory(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.history$')] = ChannelsHistory


class ChannelsInfo(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.info$')] = ChannelsInfo


class ChannelsInvite(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.invite$')] = ChannelsInvite


class ChannelsJoin(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.join$')] = ChannelsJoin


class ChannelsKick(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.kick$')] = ChannelsKick


class ChannelsLeave(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.leave$')] = ChannelsLeave


class ChannelsList(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.list$')] = ChannelsList


class ChannelsLeave(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.leave$')] = ChannelsLeave


class ChannelsMark(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.mark$')] = ChannelsMark


class ChannelsRename(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.rename$')] = ChannelsRename


class ChannelsSetPurpose(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.setPurpose$')] = ChannelsSetPurpose


class ChannelsSetTopic(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/channels.setTopic$')] = ChannelsSetTopic


class ChannelsUnarchive(RestObject):
    pass
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
        return FromUrl('https://slack.com/api/chat.delete', self._requests)(data=self.params).post()

    def post_message(self, channel, text, **kwargs):
        """ https://api.slack.com/methods/chat.postMessage
        """
        if not channel.startswith('#'):
            channel = '#' + channel
        self.params.update({
            'channel': channel,
            'text':    text,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/chat.postMessage', self._requests)(data=self.params).post()

    def update(self, channel, text, ts):
        """ https://api.slack.com/methods/chat.update
        """
        self.params.update({
            'channel': channel,
            'text':    text,
            'ts':      ts,
            })
        return FromUrl('https://slack.com/api/chat.update', self._requests)(data=self.params).post()
_url_to_api_object[re.compile(r'^https://slack.com/api/chat$')] = Chat


class ChatDelete(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/chat.delete$')] = ChatDelete


class ChatPostMessage(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/chat.postMessage$')] = ChatPostMessage


class ChatUpdate(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/chat.update$')] = ChatUpdate


# ================================================================================================
# emoji
# ================================================================================================
class Emoji(ApiBase):
    @property
    def list(self):
        return FromUrl('https://slack.com/api/emoji.list', self._requests)(data=self.params).get()
_url_to_api_object[re.compile(r'^https://slack.com/api/emoji$')] = Emoji


class EmojiList(RestObject):
    pass
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
        return FromUrl('https://slack.com/api/files.info', self._requests)(data=self.params).get()

    def list(self, **kwargs):
        """ https://api.slack.com/methods/files.list
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/files.list', self._requests)(data=self.params).get()

    def upload(self, **kwargs):
        """ https://api.slack.com/methods/files.upload
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/files.upload', self._requests)(data=self.params).post()

    def delete(self, **kwargs):
        """ https://api.slack.com/methods/files.delete
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/files.delete', self._requests)(data=self.params).post()
_url_to_api_object[re.compile(r'^https://slack.com/api/files$')] = Files


class FilesInfo(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/files.info$')] = FilesInfo


class FilesList(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/files.list$')] = FilesList


class FilesUpload(RestObject):
    def post(self):
        """ @override
        """
        files = {}
        files = {'file': open(self.params['data']['file'])}
        return self._requests.post(self.url, params=self.params['data'], files=files)
_url_to_api_object[re.compile(r'^https://slack.com/api/files.upload$')] = FilesUpload


class FilesDelete(RestObject):
    def post(self):
        """ @override
        """
        files = {}
        files = {'file': open(self.params['data']['file'])}
        return self._requests.post(self.url, params=self.params['data'], files=files)
_url_to_api_object[re.compile(r'^https://slack.com/api/files.delete$')] = FilesDelete

# ================================================================================================
# groups
# ================================================================================================
class Groups(ApiBase):
    def archive(self, group_name):
        """ https://api.slack.com/methods/groups.archive
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            })
        return FromUrl('https://slack.com/api/groups.archive', self._requests)(data=self.params).post()

    def close(self, group_name):
        """ https://api.slack.com/methods/groups.close
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            })
        return FromUrl('https://slack.com/api/groups.close', self._requests)(data=self.params).post()

    def create(self, group_name):
        """ https://api.slack.com/methods/groups.create
        """
        self.params.update({'name': group_name})
        return FromUrl('https://slack.com/api/groups.create', self._requests)(data=self.params).post()

    def list(self, **kwargs):
        """ https://api.slack.com/methods/groups.list
        """
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/groups.list', self._requests)(data=self.params).get()

    def create_child(self, group_name):
        """ https://api.slack.com/methods/groups.createChild
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            })
        return FromUrl('https://slack.com/api/groups.createChild', self._requests)(data=self.params).post()

    def history(self, group_name, **kwargs):
        """ https://api.slack.com/methods/groups.history
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/groups.history', self._requests)(data=self.params).get()

    def invite(self, group_name, user):
        """ https://api.slack.com/methods/groups.invite
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            'user':    user,
            })
        return FromUrl('https://slack.com/api/groups.invite', self._requests)(data=self.params)

    def kick(self, group_name, user):
        """ https://api.slack.com/methods/groups.kick
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            'user':    user,
            })
        return FromUrl('https://slack.com/api/groups.kick', self._requests)(data=self.params).post()

    def leave(self, group_name):
        """ https://api.slack.com/methods/groups.leave
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            })
        return FromUrl('https://slack.com/api/groups.leave', self._requests)(data=self.params).post()

    def mark(self, group_name, ts):
        """ https://api.slack.com/methods/groups.mark
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            'ts':      ts,
            })
        return FromUrl('https://slack.com/api/groups.mark', self._requests)(data=self.params).post()

    def open(self, group_name):
        """ https://api.slack.com/methods/groups.open
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            })
        return FromUrl('https://slack.com/api/groups.open', self._requests)(data=self.params).post()

    def rename(self, group_name, new_name):
        """ https://api.slack.com/methods/groups.rename
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            'name':    new_name,
            })
        return FromUrl('https://slack.com/api/groups.rename', self._requests)(data=self.params).post()

    def set_purpose(self, group_name, purpose):
        """ https://api.slack.com/methods/groups.setPurpose
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            'purpose': purpose,
            })
        return FromUrl('https://slack.com/api/groups.setPurpose', self._requests)(data=self.params).post()

    def set_topic(self, group_name, topic):
        """ https://api.slack.com/methods/groups.setTopic
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            'topic':   topic,
            })
        return FromUrl('https://slack.com/api/groups.setTopic', self._requests)(data=self.params).post()

    def unarchive(self, group_name):
        """ https://api.slack.com/methods/groups.unarchive
        """
        group_id = self.get_group_id(group_name)
        self.params.update({
            'channel': group_id,
            })
        return FromUrl('https://slack.com/api/groups.unarchive', self._requests)(data=self.params).post()

    def all(self):
        groups = []
        for line in self.list().iter_lines():
            if line:    # JSON string.
                groups = json.loads(line).get('groups')
        return groups

    def get_group_id(self, group_name):
        for group in self.all():
            if group['name'] == group_name:
                return group['id']
        return ''

_url_to_api_object[re.compile(r'^https://slack.com/api/groups$')] = Groups


class GroupsArchive(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.archive$')] = GroupsArchive


class GroupsList(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.list$')] = GroupsList


class GroupsClose(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.close$')] = GroupsClose


class GroupsCreate(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.create$')] = GroupsCreate


class GroupsCreateChild(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.createChild$')] = GroupsCreateChild


class GroupsHistory(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.history$')] = GroupsHistory


class GroupsInvite(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.invite$')] = GroupsInvite


class GroupsKick(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.kick$')] = GroupsKick


class GroupsLeave(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.leave$')] = GroupsLeave


class GroupsMark(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.mark$')] = GroupsMark


class GroupsOpen(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.open$')] = GroupsOpen


class GroupsRename(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.rename$')] = GroupsRename


class GroupsSetPurpose(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.setPurpose$')] = GroupsSetPurpose


class GroupsSetTopic(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.setTopic$')] = GroupsSetTopic


class GroupsUnarchive(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/groups.unarchive$')] = GroupsUnarchive


# ================================================================================================
# im
# ================================================================================================
class Im(ApiBase):
    def list(self):
        """ https://api.slack.com/methods/im.list
        """
        return FromUrl('https://slack.com/api/im.list', self._requests)(data=self.params).get()

    def close(self, channel):
        """ https://api.slack.com/methods/im.close
        """
        self.params.update({
            'channel': channel,
            })
        return FromUrl('https://slack.com/api/im.close', self._requests)(data=self.params).post()

    def history(self, channel, **kwargs):
        """ https://api.slack.com/methods/im.history
        """
        self.params.update({
            'channel': channel,
            })
        if kwargs:
            self.params.update(kwargs)
        return FromUrl('https://slack.com/api/im.history', self._requests)(data=self.params).get()

    def mark(self, channel, ts):
        """ https://api.slack.com/methods/im.mark
        """
        self.params.update({
            'channel': channel,
            'ts':      ts,
            })
        return FromUrl('https://slack.com/api/im.mark', self._requests)(data=self.params).post()

    def open(self, user):
        """ https://api.slack.com/methods/im.history
        """
        self.params.update({
            'user': user,
            })
        return FromUrl('https://slack.com/api/im.open', self._requests)(data=self.params).post()
_url_to_api_object[re.compile(r'^https://slack.com/api/im$')] = Im


class ImClose(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/im.close$')] = ImClose


class ImHistory(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/im.history$')] = ImHistory


class ImList(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/im.list$')] = ImList


class ImMark(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/im.mark$')] = ImMark


class ImOpen(RestObject):
    pass
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
        return FromUrl('https://slack.com/api/oauth.access', self._requests)(data=self.params).post()
_url_to_api_object[re.compile(r'^https://slack.com/api/oauth$')] = OAuth


class OAuthAccess(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/oauth.access$')] = OAuth


# ================================================================================================
# rtm
# ================================================================================================
class Rtm(ApiBase):
    @property
    def start(self):
        """ https://api.slack.com/methods/rtm.start
        """
        return FromUrl('https://slack.com/api/rtm.start', self._requests)(data=self.params).get()
_url_to_api_object[re.compile(r'^https://slack.com/api/rtm$')] = Rtm


class RtmStart(RestObject):
    """ https://api.slack.com/rtm
    """
    def lasting(self, interval=1):
        # TODO: Return json per interval.
        import time
        while True:
            print(self.get().json())
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
        return FromUrl(self.url, self._requests)(data=self.params).get()


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
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/search.all$')] = SearchAll


class SearchFiles(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/search.files$')] = SearchFiles


class SearchMessages(RestObject):
    pass
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
        return FromUrl('https://slack.com/api/stars.list', self._requests)(data=self.params).get()
_url_to_api_object[re.compile(r'^https://slack.com/api/stars$')] = Stars


class StarsList(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/stars.list$')] = StarsList


# ================================================================================================
# users
# ================================================================================================
class Users(ApiBase):
    def get_presence(self, user_name):
        """ https://api.slack.com/methods/users.getPresence
        """
        user_id = self.get_id_by_name(user_name)
        self.params.update({
            'user': user_id,
            })
        return FromUrl('https://slack.com/api/users.getPresence', self._requests)(data=self.params).get()

    def set_presence(self, presence):
        """ https://api.slack.com/methods/users.setPresence
        """
        if presence not in ['auto', 'away']:
            presence = 'auto'
        self.params.update({
            'presence': presence,
            })
        return FromUrl('https://slack.com/api/users.setPresence', self._requests)(data=self.params).post()

    def info(self, user):
        """ https://api.slack.com/methods/users.info
        """
        self.params.update({
            'user': user,
            })
        return FromUrl('https://slack.com/api/users.info', self._requests)(data=self.params).get()

    @property
    def list(self):
        """ https://api.slack.com/methods/users.list
        """
        return FromUrl('https://slack.com/api/users.list', self._requests)(data=self.params).get()

    def set_active(self, user):
        """ https://api.slack.com/methods/users.setActive
        """
        self.params.update({
            'user': user,
            })
        return FromUrl('https://slack.com/api/users.setActive', self._requests)(data=self.params).post()

    def get_info_by_name(self, user_name):
        user_id = self.get_id_by_name(user_name)
        return self.info(user_id)

    def get_name_by_id(self, user_id):
        members = self.list.json()['members']
        for member in members:
            if member.get('id') == user_id:
                return member['name']
        return ''

    def get_id_by_name(self, user_name):
        if not user_name:
            return ''
        members = self.list.json()['members']
        for member in members:
            if member.get('name') == user_name:
                return member['id']
        return ''
_url_to_api_object[re.compile(r'^https://slack.com/api/users$')] = Users


class UsersGetPresence(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/users.getPresence$')] = UsersGetPresence


class UsersSetPresence(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/users.setPresence$')] = UsersSetPresence


class UsersInfo(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/users.info$')] = UsersInfo


class UsersList(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/users.list$')] = UsersList


class UsersSetActive(RestObject):
    pass
_url_to_api_object[re.compile(r'^https://slack.com/api/users.setActive$')] = UsersSetActive
