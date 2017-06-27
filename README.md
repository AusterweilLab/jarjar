# jarjar

Jarjar is a collection of scripts that lets you programmatically send notifications to your Slack instance.

# What can jarjar do for me?

## In bash:

- Echo statements to your Slack instance: `jarjar -e -u #slack-team -m "Hi, Slack users!"`
- Notify you when your code is does running: `jarjar -u @slack-user -m "Your job is finished!" python my-script.py`

## In python:

- Echo statements to your Slack instance in your Python code: 

```
    from jarjar import jarjar
    jj = jarjar("#slack-team")
    jj.post("Arbitrary message!")
```

# How do I install jarjar?

- To install the bash script, place `sh/jarjar` in your path.
- To install the python script, place the `python` directory to your python modules directory and rename it to `jarjar`

# How do I configure jarjar?

- For both python and bash scripts, it is recommended that you set your Slack webhook directly in the code. Simply replace `your-webhook-here` with your Slack webhook URL, e.g. `https://hooks.slack.com/services/your-webhook`
- You can also specify a default username, message, and webhook by modifying the appropriate lines in `sh/jarjar`
- The bash script also allows you to configure a custom message, username, and webhook by specificying them in `~/.jarjar`. See `sh/.jarjar` for an example
- You can override a webhook in your python code, e.g., `jj = jarjar("#slack-team", url="your-webhook-here")`

# Additional options for bash jarjar
- You can override the webhook using `-w your-webhook-here`
- You can override the username using `-u username` (username can be a @username or #channel)
- You can override the message using `-m "your message here"`
- By default (without the `-e` flag), bash jarjar launches a screen with your script (which terminates when your script ends). You can immediately attach this screen using `-r` (and detach using `ctrl+A+D` as usual). This is useful in case your Python code has an error, which will prevent the screen from terminating. You can always resume a screen launched by jarjar by finding the appropriate PID: `screen -ls` and `screen -r PID`
