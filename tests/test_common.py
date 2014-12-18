import os, os.path
import ConfigParser

package = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
import slack


class TestSlack(object):
    def setup(self):
        self.set_up_config()
        self.set_up_slack()

    def set_up_config(self):
        search_paths = [os.path.expanduser('~/.slack'), '/etc/slack']

        self.config = ConfigParser.ConfigParser()
        self.config.read(search_paths)

        if self.config.has_section('Slack'):
            self.access_token = self.config.get('Slack', 'token')
        elif 'SLACK_TOKEN' in os.environ:
            self.access_token = os.environ['SLACK_TOKEN']
        else:
            print('Authorization token not detected! The token is pulled from '\
                '~/.slack, /etc/slack, or the environment variable SLACK_TOKEN.')
        self.test_channel = self.config.get('Slack', 'test-channel')

    def set_up_slack(self):
        self.slack = slack.Slack(self.access_token)

