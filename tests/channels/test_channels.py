import pytest
from tests.test_common import TestSlack


class TestChannels(TestSlack):
    def test_channels(self):
        assert self.slack.channels

    @pytest.mark.skipif("True")
    def test_channels_archive(self):
        self.slack.channels.archive(self.test_channel).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_create(self):
        self.slack.channels.create(self.test_channel_name).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_history(self):
        self.slack.channels.history(self.test_channels).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_info(self):
        self.slack.channels.info(self.test_channels).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_invite(self):
        self.slack.channels.info(self.test_channels, self.test_user).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_join(self):
        self.slack.channels.join(self.test_user).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_kick(self):
        self.slack.channels.kick(self.test_channel, self.test_user).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_leave(self):
        self.slack.channels.leave(self.test_channel).status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_list(self):
        self.slack.channels.list.status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_mark(self):
        self.slack.channels.mark(self.test_channel, ts='').status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_rename(self):
        self.slack.channels.rename(self.test_channel, new_name='New test channel').status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_set_purpose(self):
        self.slack.channels.set_purpose(self.test_channel, 'New purpose').status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_set_topic(self):
        self.slack.channels.set_topic(self.test_channel, 'New topic').status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_unarchive(self):
        self.slack.channels.unarchive(self.test_channel).status_code == 200
