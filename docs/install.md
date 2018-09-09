# Installing jarjar

## Just use pip.

We're on [pypi](https://pypi.org/project/jarjar/).

```shell
pip install jarjar
```

## Config File

You can use jarjar without a config file, but you'll need to tell it your slack
webhook and channel each time.

You don't want to live that way.

Jarjar looks to a special config file for a default webhook, channel, and
message values. You can over-ride anything in the config file any time but its
nice not to have your webhook in each script, amirite??

The file looks like:

```sh
channel='@username'
message='Custom message'
webhook='https://hooks.slack.com/services/your/teams/webhook'
```

Jarjar looks for values in descending order of priority:

1. Any argument provided to `jarjar().text()` or `jarjar().attach()` at runtime.
2. Any argument provided to `jarjar()` at initialization.
3. Defaults within a file at a user-specified path (`config='...'`), provided to
   `jarjar()` at initialization.
4. Defaults within a config file ``.jarjar``, in the working directory.
5. Defaults within ``.jarjar``, located in the user's home directory (`~`).

## Configuring Slack

For this to work in the first place, you need to [set up a slack webhook for your team](https://my.slack.com/apps/A0F7XDUAZ-incoming-webhooks).

While you're doing that, you can also specify a custom name and custom icon. We named our webhook robot `jar-jar`, and we used [this icon](http://i.imgur.com/hTHrg6i.png), so messages look like this:

![](http://i.imgur.com/g9RG16j.png)

### A note about old vs new-style webhooks

These days slack suggests users configure webhooks through an app, but you can still set up an [old-style webhook](https://my.slack.com/apps/A0F7XDUAZ-incoming-webhooks). Jarjar was written to use the old style-hooks, but both kinds will work - _with one caveat_.

Under the new webhook setup, individual webhooks send messages to a single channel, so Jarjar's `channel='@me'` functionality will not work. Jarjar expects to use an old-style hook so it requires a channel to be specified even if you are using a new-style hook (sorry about that!).
