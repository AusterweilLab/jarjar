# Jarjar slack notifier

Jarjar is a collection of scripts that lets you programatically send notifications to your Slack team. 

# What can jarjar do for me?

Here are some things _we_ use it for:

- Notify users when their jobs (simulations, backups, etc) are completed.
- Combine jarjar with cron to send out daily positive vibes.
- Sending reminders to a group.

## But How?

We have designed two interfaces into jarjar: a shell command and a Python Module.

#The Shell Command

The [`sh/`](sh/) directory contains a shell command `jarjar` and a configuration file `.jarjar`.

Fill the configuration file out with useful defaults. Critically, you'll want to paste in your [Slack Webook](https://api.slack.com/incoming-webhooks) so that jarjar knows where to send the message. Then put the configuration file in your home directory (`~/`), that's where jarjar will look for it. Don't worry, you can override those defaults later.

Then, make sure the `jarjar` _script_ is in your path. After that, you can use it like so:

```sh
# echo the default message to the default channel
./jarjar -e

# echo a message to the #general channel
./jarjar -e -u "#general" -m "Hi, everyone!!"

# Send yourself a notification when a script is completed
./jarjar -u "@username" -m "Your job is finished!" python my-script.py

# send a message to the non-default slack team
./jarjar -e "@username" -m "Hi!" -w "their-webhook-url"
```

## Modifiers

| Modifier | Description | 
|   ---    |     ---     |
|   `-e`   | Echo the message. If this flag is not included, jarjar wait until a provided process is completed to send the message. By default (without the `-e` flag), jarjar launches a screen with your script (which terminates when your script ends). You can always resume a screen launched by jarjar by finding the appropriate PID: `screen -ls` and `screen -r PID`. |
|   `-m`   | Message to be sent |
|   `-u`   | Username (or channel). Usernames must begin with `@`, channels with `#`. |
|   `-w`   | Webhook for the Slack team. |

# The Python Module

This module is designed to be included at the end of a Python script, and has similar functionality as the shell command. Importing the jarjar module provides a simple class, which is initialized by a Slack webhook. The `post` method allows you to send a message to a specified channel.

Installation is simple: make sure the [`python/jarjar`](python/jarjar/) folder is on your current path (e.g., copy it to your working directory, or your modules directory). Then you can use it as follows:

```python
from jarjar import jarjar
jj = jarjar("slack-webhook-url") # initialize with your webhook
jj.post("Hi!", "@username") # send a message to a user
jj.post("Hi!", "#channel") # send a message to a channel
```


# What is my team's webhook?

You'll need to configure [Incoming Webhooks](https://api.slack.com/incoming-webhooks) for your Slack team. You need to specify a default channel (which jarjar overrides), and Slack will give you a webhook url. That's it! 

When you're setting things up, you can also specify a custom name and custom icon. We named our webhook robot `jar-jar`, and we used [this icon](http://i.imgur.com/hTHrg6i.png), so messages look like this:

![](http://i.imgur.com/g9RG16j.png)

