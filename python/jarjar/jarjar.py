import requests
import json

class jarjar():
    def __init__(self, channel=None, url=None):
    	self.default_channel = channel
        self.default_url = url
        self.headers ={'Content-Type': 'application/json'}

    def __call__(self, text, **kwargs):
        """
        Allow functional-style usage, like so:
        jj = jarjar()
        jj('Hi', channel = '@nolan', url = url)
        """
        return self.post(text, **kwargs)

    def post(self, text, channel=None, url=None):
        """
        Generic method to send a message to slack. 
        The default channel and url may be overridden
        """

    	# make sure channel and URL are _somewhere_
    	if [self.default_channel, channel] == [None, None]:
    		raise Exception('No channel provided!')
    	if [self.default_url, url] == [None, None]:
    		raise Exception('No webhook url provided!')

    	# use defaults if not overridden
    	if channel is None: channel = self.default_channel
    	if url is None: url = self.default_url

        payload = json.dumps({"text": text, "channel": channel})
        response = requests.post(url, data=payload, headers=self.headers)
        return response

    def set_url(self, url):
        self.default_url = url
        
    def set_channel(self, channel):
        self.default_channel = channel


