# Installing jarjar

## Just use pip.

We're on [pypi](https://pypi.org/project/jarjar/).

```shell
pip install jarjar
```

## Config File

You can use jarjar without a config file, but you'll need to tell it your slack webhook and channel each time.

You don't want to live that way.

Jarjar looks for a special file in your user home `~/.jarjar` for default webhook, channel, and/or message. You can over-ride anything in there pretty much any time you want.

```sh
channel='@username'
message='Custom message'
webhook='https://hooks.slack.com/services/your/teams/webhook'
```

## Configuring Slack

For this to work in the first place, you need to [set up a slack webhook for your team](https://api.slack.com/incoming-webhooks).

While you're doing that, you can also specify a custom name and custom icon. We named our webhook robot `jar-jar`, and we used [this icon](http://i.imgur.com/hTHrg6i.png), so messages look like this:

![](http://i.imgur.com/g9RG16j.png)
