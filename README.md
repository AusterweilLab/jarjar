# Jarjar Slack Notifier

Jarjar is a python utility that makes it easy to send slack notifications to your teams. You can import it as a python module or use our command line tool.

[![Documentation Status](https://readthedocs.org/projects/jarjar/badge/?version=v3.0)](https://readthedocs.org/projects/jarjar/badge/?version=v3.0) [![PyPI version](https://badge.fury.io/py/jarjar.svg)](https://badge.fury.io/py/jarjar)


## What can jarjar do for me?

Jarjar was developed at the [Austerweil Lab at UW-Madison](http://alab.psych.wisc.edu/) as a tool for scientists. We use it for all sorts of things, such as:

1. Sending a message so that we know when long-running processes have finished.

![](docs/img/simulations-complete.png)

2. Sending notices when scheduled tasks have failed.

![](docs/img/backups-failed.png)

3. Sending out daily positive vibes.

![](docs/img/positive-vibes.png)

## Quickstart

[Installation](docs/install.md) is simple!

```shell
pip install jarjar
```

My guess is that you'll want to create jarjar's config file, `~/.jarjar`. This tells jarjar what you'd like to use as a default for your slack team's webhook, the channel to post to, and the message it sends. Don't worry, you can over-ride these anytime.

Edit this snippet and add it to `~/.jarjar`:

```shell
channel='@username'
message='Custom message'
webhook='https://hooks.slack.com/services/your/teams/webhook'
```

If you don't know your team's webhook, you might have to [make one](https://api.slack.com/incoming-webhooks)

### Python API

Use the jarjar python api like:

```python
from jarjar import jarjar

# initialize a jarjar object
jj = jarjar() # defaults from .jarjar
jj = jarjar(channel='#channel', webhook='slack-webhook-url')
jj = jarjar(webhook='slack-webhook-url')

# send a text message
jj.text('Hi!')
jj.text('Hi!', channel=["@jeffzemla", "#channel"])

# send an attachment
jj.attach({'meesa': 'jarjar binks'}), text='Hello!')
```

### Command Line Tool

We also made a [command line tool](docs/clt.md) for use outside of python scripts. The command line tool adds functionality to execute processes and send messages when they are complete.

```shell
jarjar sleep 1 -m 'Meesa took a nap!'
```

And then in your slack team:

![](docs/img/nap.png)

Custom attachments are not supported in the CLT at this time, but everything else is:

```sh
jarjar -m 'Meesa jarjar binks!'
jarjar -m 'Hi, everyone!!' --webhook '<your-url>' -c '#general'
```

## Documentation

We're on [Read The Docs](http://jarjar.readthedocs.io/en/latest/)!

## Having Trouble? Or a feature request?

We are terrible developers and you'll probably run into all sorts of problems. Don't be shy, [file an issue on github](https://github.com/AusterweilLab/jarjar/issues/new)!
