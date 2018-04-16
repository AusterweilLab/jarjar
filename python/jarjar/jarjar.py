import requests
import json
import time
import os
import imp

class jarjar():

    def __init__(self, channel=None, webhook=None, message=None):

        # read config file, set defaults
        self._read_config()
        self._set_defaults(channel=channel, webhook=webhook, message=message)

        # headers for post request
        self.headers = {'Content-Type': 'application/json'}

    def _set_defaults(self, channel=None, webhook=None, message=None):
        """
        Set the default channel and webhook and message
        This could be a little drier....
        """

        # set default channel
        if channel is None:
            self.default_channel = self.cfg_channel
        else:
            self.default_channel = channel

        # same thing for webhook
        if webhook is None:
            self.default_webhook = self.cfg_webhook
        else:
            self.default_webhook = webhook

        # same thing for message
        if message is None:
            self.default_message = self.cfg_message
        else:
            self.default_message = message

    def _read_config(self):
        """
        Read the .jarjar file for defaults.
        """

        # get .jarjar path
        filename = os.path.join(os.path.expanduser('~'), '.jarjar')
        
        # make empty .jarjar if needed
        if not os.path.exists(filename):
            open(filename, 'a').close()

        # load config
        cfg = imp.load_source('_jarjar', filename)

        # assign variables
        for field in ['channel','webhook','message']:

            # read from config, or set to none
            if hasattr(cfg, field): 
                data = getattr(cfg, field)
            else: 
                data = None

            # set value
            setattr(self, 'cfg_%s' % field, data)


    def _args_handler(self, channel, webhook, message):
        """
        Decide to use the default or provided arguments
        """

        # make sure channel and URL are _somewhere_
        if [self.default_channel, channel] == [None, None]:
            raise Exception('No channel provided!')

        if [self.default_webhook, webhook] == [None, None]:
            raise Exception('No webhook url provided!')

        # use defaults if not overridden
        if channel is None: channel = self.default_channel
        if webhook is None: webhook = self.default_webhook
        if message is None: message = self.default_message

        return channel, webhook, message

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

    def text(self, message, **kwargs):
        """
        Send a message, without attachments. This is a wrapper around
        self.post
        """
        return self.post(message = message, **kwargs)

    def post(self, message=None, attach=None, channel=None, webhook=None):
        """
        Generic method to send a message to slack. Defaults may be overridden.
        The user may specify text or attachments.
        """

        # get channel and webhook and message
        channel, webhook, message = self._args_handler(channel, webhook, message)

        # return if there is nothing to send
        if [message, attach] == [None, None]: return None

        # recursively post to all channels in array of channels
        if isinstance(channel, list):
            status=[]
            for c in channel:
                status.append(self.post(message=message, attach=attach, channel=c, url=webhook))
            return status

        # construct a payload
        payload = dict(channel = channel)
        
        # add text and attachments if provided
        if message is not None:
            payload['text'] = message

        if attach is not None:
            payload['attachments']= self._attachment_formatter(attach)

        # convert payload to json and return
        payload = json.dumps(payload)
        return requests.post(webhook, data=payload, headers=self.headers)

    def set_webhook(self, webhook):
        self.default_webhook = webhook
        
    def set_channel(self, channel):
        self.default_channel = channel

    def set_message(self, message):
        self.default_message = message
