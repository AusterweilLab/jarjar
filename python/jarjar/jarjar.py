import requests
import json
import time

class jarjar():
    def __init__(self, channel=None, url=None):
    	self.default_channel = channel
        self.default_url = url
        self.headers ={'Content-Type': 'application/json'}

    def _args_handler(self, channel, url):
        """
        Decide to use the default or provided arguments
        """

        # make sure channel and URL are _somewhere_
        if [self.default_channel, channel] == [None, None]:
            raise Exception('No channel provided!')
        if [self.default_url, url] == [None, None]:
            raise Exception('No webhook url provided!')
       
        # use defaults if not overridden
        if channel is None: channel = self.default_channel
        if url is None: url = self.default_url

        return channel, url

    @staticmethod
    def _attachment_formatter(attach):
        """
        Convert a dict, fields, into a a correctly-formatted
        attachment object for Slack.
        """
        attachments = dict(
                fallback = "New attachments are ready!",
                color =  "#36a64f",
                ts = time.time(),
                fields = []
             )

        field_array = []
        for key in attach:
            if isinstance(attach[key], str): outval = attach[key]
            else: outval = str(attach[key])
            attachments['fields'].append(dict(
                title = key, 
                value = outval, 
                short = len(outval) < 20
            ))

        return [attachments]

    def attach(self, attach, **kwargs):
        """
        Send an attachment, without text. This is a wrapper around
        self.post
        """
        return self.post(attach = attach, **kwargs)

    def text(self, text, **kwargs):
        """
        Send a message, without attachments. This is a wrapper around
        self.post
        """
        return self.post(text = text, **kwargs)

    def post(self, text=None, attach=None, channel=None, url=None):
        """
        Generic method to send a message to slack. Defaults may be overridden.
        The user may specify text or attachments.
        """

        # return if there is nothing to send
        if [text, attach] == [None, None]: return None

        # get channel and URL
    	channel, url = self._args_handler(channel, url)

        # construct a payload
        payload = dict(channel = channel)

        # add text and attachments if provided
        if text is not None:
            payload['text'] = text

        if attach is not None:
            payload['attachments']= self._attachment_formatter(attach)

        # convert payload to json and return
        payload = json.dumps(payload)
        return requests.post(url, data=payload, headers=self.headers)

    def set_url(self, url):
        self.default_url = url
        
    def set_channel(self, channel):
        self.default_channel = channel
