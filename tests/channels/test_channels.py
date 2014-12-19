import pytest
from tests.test_common import TestSlack

class TestChannels(TestSlack):
    def setup(self):
        self.channels = self.slack.channels

    def test_channels(self):
        assert self.slack.channels

    @pytest.mark.skipif("True")
    def test_channels_archive(self):
        self.channels.archive(self.test_channel).post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_create(self):
        self.channels.create(self.test_channel_name).post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_history(self):
        self.channels.history(self.test_channels).get().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_info(self):
        self.channels.info(self.test_channels).get().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_invite(self):
        self.channels.info(self.test_channels, self.test_user).post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_join(self):
        self.channels.join(self.test_user).post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_kick(self):
        self.channels.kick(self.test_channel, self.test_user).post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_leave(self):
        self.channels.leave(self.test_channel).post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_list(self):
        self.channels.list.get().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_mark(self):
        self.channels.mark(self.test_channel, ts='').post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_rename(self):
        self.channels.rename(self.test_channel, new_name='New test channel').post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_set_purpose(self):
        self.channels.set_purpose(self.test_channel, 'New purpose').post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_set_topic(self):
        self.channels.set_topic(self.test_channel, 'New topic').post().status_code == 200

    @pytest.mark.skipif("True")
    def test_channels_unarchive(self):
        self.channels.unarchive(self.test_channel).post().status_code == 200
