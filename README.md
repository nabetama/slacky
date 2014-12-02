# pysla

A Python package for Slack's `preview release of the Slack API`.

- [Slack API](https://api.slack.com/)

## Installation

pysla can either be installed from PyPI.

    pip install slack


Or from source

    python setup.py install

PyPI: https://pypi.python.org/pypi/pysla
source: https://github.com/nabetama/pysla


## Usage

First, create a pysla object with your [token](https://api.slack.com/#auth).

    slack = Slack("YOUR TOKEN")

There are several root links

    slack.apitest() # {'ok': true}

