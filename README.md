# slacky

A Python package for Slack's [JSON REST API](https://api.slack.com/).

## Installation

```sh
pip install slacky
```

## Examples

```python

from slacky import Slacky

slack = Slacky(token='<Your slack api token>')

# Send a message to #general channel.
slack.chat.post_message('#general', 'Hello from slacky')
# '#' is not necessary with channel name.
slack.chat.post_message('general', 'Hello from slacky')

# If you want a JSON result.
print slack.chat.post_message('general', 'Hello from slacky').json()
> => {u'ok': True,  u'ts': u'1234567890.000001',  u'channel': u'XXXXXXXXX'}

# Get timeline at 'general' channel.
for msg in slacky.timeline(channel_name='general', count=4):
    print(msg)

# Create a channel where name is "slackers".
slack.channels.create('slackers')

# Create a private group.
slack.groups.create('slackers')

# Get users list.
slack.users.list.json()['members']

# Get user info.
slack.users.get_info_by_name('nabetama')

# Upload a file.
slack.files.upload(file='hello.png')

```

[![wercker status](https://app.wercker.com/status/5d1ccee5911286b664b05d1a697987d2/m "wercker status")](https://app.wercker.com/project/bykey/5d1ccee5911286b664b05d1a697987d2)
